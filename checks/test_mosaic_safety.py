"""Owned format fixtures and actual process/file boundaries for current runtime."""
import argparse
import io
import os
from pathlib import Path
import struct
import subprocess
import sys
import time
from types import SimpleNamespace

import pytest
from policymosaic import profile_decoder as profiles
from policymosaic import string_bytecode as strings
from policymosaic import regex_bytecode as regex
from policymosaic import regex_graph
from policymosaic import rule_graph
from policymosaic import filter_decoder
from policymosaic import firmware_helper as firmware
from policymosaic.safety import (PolicyFormatError, ProfileReader, read_exact, read_local,
    write_exclusive, safe_component, ReportBuffer, run_tool, bounded_analysis,
    WorkBudget, _budget, checked_add, checked_multiply, c_content)

ROOT = Path(__file__).resolve().parents[1]
ALLOW = bytes((1,0,0,0,0,0,0,0))
DENY = bytes((1,1,0,0,0,0,0,0))
BRANCH = bytes((0,13,6,0,1,0,0,0))


def fixture(nodes=(ALLOW,DENY), table=(0,1), names=()):
    kind = 0x8000 if names else 0
    header = struct.pack('<HHBBBxHHHH', kind,len(nodes),len(table),0,0,len(names),0,0,0)
    data = profiles.parse_profile(io.BytesIO(header),argparse.Namespace(release='17'))
    wire = bytearray(data.base_addr)
    wire[:16] = header
    metadata = bytearray()
    if names:
        for index, name in enumerate(names):
            raw = name.encode('utf-8')
            offset = len(metadata)//8
            metadata.extend(struct.pack('<H',len(raw)+1)+raw+b'\0')
            metadata.extend(b'\0'*(-len(metadata)%8))
            start=data.profiles_offset+index*(len(table)*2+4)
            wire[start:start+len(table)*2+4]=struct.pack('<HH'+'H'*len(table),offset,0,*table)
    else:
        wire[data.profiles_offset:data.profiles_offset+len(table)*2]=struct.pack('<'+'H'*len(table),*table)
    wire[data.operation_nodes_offset:data.base_addr]=b''.join(nodes)
    wire.extend(metadata)
    return bytes(wire)


def cli(folder, raw=None, *, extra=(), filename='input.bin', labels='default\nfile-read*\n'):
    folder.mkdir(exist_ok=True)
    source=folder/filename
    if raw is not None: source.write_bytes(raw)
    operations=folder/'operations.txt';operations.write_text(labels)
    before=source.read_bytes() if source.is_file() and not source.is_symlink() else None
    env=dict(os.environ,PYTHONPATH=str(ROOT/'src'),PYTHONDONTWRITEBYTECODE='1')
    result=subprocess.run([sys.executable,'-m','policymosaic.profile_decoder','-r','17','-o',str(operations),'-d',str(folder),*extra,str(source)],cwd=folder,env=env,capture_output=True,timeout=4)
    if before is not None: assert source.read_bytes()==before
    assert not (folder/'reverse.log').exists()
    return result


def test_actual_local_sbpl_and_c_reports(tmp_path):
    sb=cli(tmp_path/'scheme',fixture())
    assert sb.returncode==0,sb.stderr
    assert (tmp_path/'scheme/input.sb').read_text().startswith('(version 1)\n(allow default)\n(deny ')
    assert (tmp_path/'scheme/input.sb').stat().st_mode & 0o777==0o600
    c=cli(tmp_path/'c',fixture(),extra=('--c_output',))
    assert c.returncode==0,c.stderr
    assert 'return deny(' in (tmp_path/'c/input.c').read_text()


def test_actual_nonterminal_graph_and_same_node_reuse(tmp_path):
    raw=fixture((DENY,ALLOW,BRANCH),(0,2,2))
    result=cli(tmp_path,raw,labels='default\nfile-read*\nfile-write*\n')
    assert result.returncode==0,result.stderr
    output=(tmp_path/'input.sb').read_text()
    assert 'file-read*' in output and 'file-write*' in output and output.count('socket-protocol 6')==2


@pytest.mark.parametrize('length',range(40))
def test_actual_cli_all_short_profile_boundaries(tmp_path,length):
    result=cli(tmp_path,fixture()[:length])
    assert result.returncode==2
    assert b'Traceback' not in result.stderr
    assert not list(tmp_path.glob('*.sb'))


@pytest.mark.parametrize('kind',['directory','link','fifo'])
def test_actual_cli_rejects_nonregular_inputs(tmp_path,kind):
    source=tmp_path/'input.bin'
    if kind=='directory':source.mkdir()
    elif kind=='link':
        (tmp_path/'target').write_bytes(fixture());source.symlink_to(tmp_path/'target')
    else:os.mkfifo(source)
    result=cli(tmp_path)
    assert result.returncode==2
    assert b'Traceback' not in result.stderr


def test_existing_reports_and_links_not_overwritten(tmp_path):
    existing=tmp_path/'input.sb';existing.write_text('KEEP')
    assert cli(tmp_path,fixture()).returncode==2
    assert existing.read_text()=='KEEP'
    existing.unlink();(tmp_path/'target').write_text('KEEP');existing.symlink_to(tmp_path/'target')
    assert cli(tmp_path,fixture()).returncode==2
    assert (tmp_path/'target').read_text()=='KEEP'


@pytest.mark.parametrize('name',['../escape','/absolute','a\\b'])
def test_bundle_profile_names_stay_inside_output_directory(tmp_path,name):
    result=cli(tmp_path,fixture(names=(name,)))
    assert result.returncode==0,result.stderr
    assert (tmp_path/(safe_component(name)+'.sb')).is_file()
    assert not (tmp_path.parent/'escape.sb').exists()


@pytest.mark.parametrize('names',[('.',),('..',),('a\nb',),('a/b','a\\b')])
def test_invalid_or_colliding_bundle_names_fail_before_reports(tmp_path,names):
    result=cli(tmp_path,fixture(names=names))
    assert result.returncode==2
    assert not list(tmp_path.glob('*.sb'))


def test_bundle_listing_uses_header_stride(tmp_path):
    result=cli(tmp_path,fixture(names=('first','second')),extra=('--print_sandbox_profiles',))
    assert result.returncode==0,result.stderr
    assert result.stdout.splitlines()==[b'first',b'second']


@pytest.mark.parametrize('nodes,table',[
    ((ALLOW,bytes((2,0,0,0,0,0,0,0))),(0,1)),
    ((ALLOW,bytes((0,13,0,0,2,0,0,0))),(0,1)),
    ((ALLOW,bytes((0,13,0,0,1,0,0,0))),(0,1)),
    ((ALLOW,DENY),(0,3)),
])
def test_unknown_invalid_and_cyclic_graphs_fail(tmp_path,nodes,table):
    result=cli(tmp_path,fixture(nodes,table))
    assert result.returncode==2
    assert b'Traceback' not in result.stderr
    assert not list(tmp_path.glob('*.sb'))


@pytest.mark.parametrize('labels',['default\n','default\ndefault\n','default\nfile\";x\n','default\n../read\n'])
def test_operations_labels_must_match_and_cannot_inject_source(tmp_path,labels):
    assert cli(tmp_path,fixture(),labels=labels).returncode==2
    assert not list(tmp_path.glob('*.sb'))


@pytest.mark.parametrize('wire',[b'\x40',b'\x41a',b'\x04',b'\x08',b'\x0b',b'\x82a',b'\x40a',b'\x40\xff\x0a'])
def test_string_truncation_and_invalid_utf8_explicit(wire):
    with pytest.raises(PolicyFormatError):strings.SandboxString().parse_byte_string(wire,[])


@pytest.mark.parametrize('wire,answer',[
    (b'\x3f\x0a',['']),
    (b'\x40a\x0f\x40b\x0a',['ab']),
    (b'\x10\x0f\x40x\x0a',['${HOME}x']),
    (b'\x40a\x06\x40b\x0a',['a','b']),
    (b'\x40a\x0a\x40b\x0a',['a','b']),
    (b'\x40a\x08\x00\x00\x40b\x0a',['ab']),
])
def test_owned_string_state_cases(wire,answer):
    assert strings.SandboxString().parse_byte_string(wire,['HOME'])==answer


def test_missing_variable_and_nested_token_rejected():
    with pytest.raises(PolicyFormatError):strings.SandboxString().parse_byte_string(b'\x10\x0a',[])
    with pytest.raises(PolicyFormatError):strings.SandboxString().parse_byte_string(b'\x40a\x40b\x0a',[])


@pytest.mark.parametrize('opcode,length',[(2,1),(47,1),(47,2),(10,1),(10,2),(0x1b,1),(0x1b,2),(0x2b,1),(0x2b,2),(0x2b,3),(0x2b,4)])
def test_all_fixed_regex_operand_truncations(opcode,length):
    with pytest.raises(PolicyFormatError):regex.parse(bytes((opcode,))+b'\0'*(length-1),0,[])


def test_unknown_regex_and_bad_targets_rejected():
    with pytest.raises(PolicyFormatError):regex.parse(b'\xff',0,[])
    with pytest.raises(PolicyFormatError):regex_graph.parse_regex(b'\0'*6+b'\x2f\xff\xff\x25\0')
    with pytest.raises(PolicyFormatError):regex_graph.parse_regex(b'\0'*5)


def test_regex_instances_are_independent_and_jump_walk_is_finite():
    first=regex_graph.Graph();second=regex_graph.Graph()
    first.canon_graph_dict[99]=[('x',99)]
    assert second.canon_graph_dict=={}
    a=regex_graph.Node('a');a.set_type_jump_forward()
    b=regex_graph.Node('b');b.set_type_jump_backward()
    terminal=regex_graph.Node('c');terminal.set_type_end()
    first.graph_dict={a:[b],b:[a,terminal],terminal:[]}
    assert first.get_character_nodes(a)==[terminal]
    assert first.find_node_type_jump(a,b,first.graph_dict)
    assert not first.find_node_type_jump(a,terminal,first.graph_dict)


def test_owned_regex_sequential_parses_do_not_reuse_canonical_state():
    first=regex_graph.parse_regex(b'\0'*6+b'\x02a\x25\0')
    second=regex_graph.parse_regex(b'\0'*6+b'\x02b\x25\0')
    assert first==['a'] and second==['b']


def test_cooperative_work_and_expansion_limits():
    token=_budget.set(WorkBudget(remaining=1))
    try:
        with pytest.raises(PolicyFormatError):rule_graph.build_operation_nodes(io.BytesIO(ALLOW*2),2)
    finally:_budget.reset(token)
    with pytest.raises(PolicyFormatError):checked_multiply('a',16*1024*1024+1)
    with pytest.raises(PolicyFormatError):checked_add([None]*65536,[1])
    with pytest.raises(PolicyFormatError):ReportBuffer().write('a'*(16*1024*1024+1))


def test_checked_reader_and_fragmented_reads():
    class Fragmented(io.BytesIO):
        def read(self,n=-1):return super().read(min(n,2))
    assert read_exact(Fragmented(b'abcdef'),6)==b'abcdef'
    source=ProfileReader(b'ab')
    with pytest.raises(PolicyFormatError):source.read(-1)
    with pytest.raises(PolicyFormatError):source.seek(3)
    with pytest.raises(PolicyFormatError):source.read(3)


def test_no_length_underflow_or_context_leak():
    fake=SimpleNamespace(base_addr=0,global_vars=[],regex_list=[],sb_ops=[])
    with filter_decoder._conversion_context(fake,False):
        with pytest.raises(PolicyFormatError):filter_decoder.get_filter_arg_string_by_offset_no_skip(io.BytesIO(b'\0\0'),0)
    assert filter_decoder._filter_context.get() is None
    with filter_decoder._conversion_context(fake,False):
        assert filter_decoder.get_filter_arg_network_address(io.BytesIO(struct.pack('<HH',261,80)),0)=='tcp4 "localhost:80"'
        assert filter_decoder.get_filter_arg_string_by_offset(io.BytesIO(b'\x03\0\x40a\x0a'),0)==['a']


def test_c_literal_escapes_control_bytes_and_quotes():
    value='a"\\\n\0场'
    encoded=c_content(value)
    assert '\n' not in encoded and '\0' not in encoded and '\\012' in encoded and '\\000' in encoded
    node=rule_graph.NonTerminalNode();node.filter='literal';node.argument=[value]
    assert node.c_repr()=='regex("'+encoded+'")'


def test_actual_helper_success_failure_timeout_output_limit_and_utf8():
    assert run_tool([sys.executable,'-c','print("ok")'],text=True)=='ok\n'
    for program,keywords,message in [
        ('import sys;sys.exit(3)',{},'failed'),
        ('import time;time.sleep(5)',{'timeout':0.05},'timed out'),
        ('import sys;sys.stdout.write("x"*8192)',{'maximum':1024},'output limit'),
        ('import sys;sys.stdout.buffer.write(b"\\xff")',{'text':True},'UTF-8'),
    ]:
        started=time.monotonic()
        with pytest.raises(PolicyFormatError,match=message):run_tool([sys.executable,'-c',program],**keywords)
        assert time.monotonic()-started<2


def test_actual_helper_descendant_pipe_timeout():
    # A parent may exit while a descendant keeps the pipe open; the deadline
    # still kills their original process group and closes descriptors.
    program='import subprocess,sys;subprocess.Popen([sys.executable,"-c","import time;time.sleep(5)"])'
    started=time.monotonic()
    with pytest.raises(PolicyFormatError,match='timed out'):run_tool([sys.executable,'-c',program],timeout=0.05)
    assert time.monotonic()-started<2


def test_firmware_span_cap_before_external_tool(monkeypatch):
    monkeypatch.setattr(firmware,'run_tool',lambda *a,**kw:pytest.fail('external tool invoked'))
    for address,size in [(0,0),(1,64*1024*1024+1),(2**64-1,4),(-1,1)]:
        with pytest.raises(PolicyFormatError):firmware.macho_read_data('not-opened',address,size)


def test_disassembly_width_address_and_contiguity():
    assert firmware.get_bytes(['1000:  1f 20 03 d5   nop','1004:  1f 20 03 d5   nop'])==(0x1000,bytes.fromhex('1f2003d5')*2)
    with pytest.raises(PolicyFormatError):firmware.get_bytes(['1000:  1f 20 03 d5   nop','1008:  1f 20 03 d5   nop'])
    with pytest.raises(PolicyFormatError):firmware.get_bytes(['1001:  1f 20 03 d5   nop'])


def test_actual_unicorn_completion_and_instruction_loop_limit():
    # Native faults stay in an independent child process, including hosts whose
    # sandbox disallows Unicorn's executable mappings. Run this gate on a host
    # permitting the declared native dependency; Linux CI does so independently.
    program = """from policymosaic.firmware_helper import Emulator
from policymosaic.safety import PolicyFormatError
with Emulator(0x1000,bytes.fromhex('1f2003d5')) as emulator:
    assert emulator._completed
try:
    with Emulator(0x1000,bytes.fromhex('00000014')): pass
except PolicyFormatError: pass
else: raise AssertionError('instruction loop was not stopped')
print('native boundary PASS')
"""
    started=time.monotonic()
    result=subprocess.run([sys.executable,'-c',program],env=dict(os.environ,PYTHONPATH=str(ROOT/'src')),capture_output=True,timeout=4)
    assert result.returncode==0,result.stderr
    assert result.stdout.strip()==b'native boundary PASS'
    assert time.monotonic()-started<4


def test_firmware_native_failure_is_reported_in_parent(monkeypatch):
    monkeypatch.setattr(firmware,'run_tool',lambda *a,**kw:(_ for _ in ()).throw(PolicyFormatError('helper process failed')))
    with pytest.raises(PolicyFormatError,match='helper process failed'):
        firmware._emulate(0x1000,bytes.fromhex('1f2003d5'),'profile')


def test_firmware_emulation_result_types_and_exact_keys(monkeypatch):
    for result in ['[]','{"reference":true,"size":1}','{"reference":1,"size":-1}','{"reference":1,"size":1,"extra":1}']:
        monkeypatch.setattr(firmware,'run_tool',lambda *a,_value=result,**kw:_value)
        with pytest.raises(PolicyFormatError):firmware._emulate(0x1000,bytes.fromhex('1f2003d5'),'profile')



def test_firmware_output_containment_and_selector_errors(tmp_path,monkeypatch):
    (tmp_path/'kernel').write_bytes(b'x')
    assert firmware._owned_output('Created kernel',tmp_path)==tmp_path/'kernel'
    with pytest.raises(PolicyFormatError):firmware._owned_output('Created /outside',tmp_path)
    with pytest.raises(PolicyFormatError):firmware.ipsw_get_out_path('nothing')
    monkeypatch.setattr(firmware,'run_tool',lambda *a,**kw:pytest.fail('external tool invoked'))
    with pytest.raises(PolicyFormatError):firmware.dl_kernel('--bad','17')
    with pytest.raises(PolicyFormatError):firmware.dl_kernel('iPhone16,1','--bad')


def test_macho_compile_failure_does_not_publish_report(tmp_path,monkeypatch):
    source=ProfileReader(fixture());data=profiles.parse_profile(source,argparse.Namespace(release='17'))
    data.global_vars=[];data.regex_list=[];data.policies=[];source.seek(data.operation_nodes_offset)
    nodes=profiles.create_operation_nodes(source,data,False)
    monkeypatch.setattr(profiles,'run_tool',lambda *a,**kw:(_ for _ in ()).throw(PolicyFormatError('helper process failed')))
    with pytest.raises(PolicyFormatError):profiles.process_profile(source,str(tmp_path/'out'),['default','file-read*'],None,(0,1),nodes,False,True)
    assert not list(tmp_path.iterdir())


def test_input_size_and_identity_guards(tmp_path,monkeypatch):
    path=tmp_path/'data';path.write_bytes(b'123')
    with pytest.raises(PolicyFormatError):read_local(path,2)
    original=os.fstat;calls=[0]
    def changed(descriptor):
        value=original(descriptor);calls[0]+=1
        if calls[0]>1:
            fields={key:getattr(value,key) for key in ['st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns','st_mode']}
            fields['st_ctime_ns']+=1
            return SimpleNamespace(**fields)
        return value
    monkeypatch.setattr(os,'fstat',changed)
    with pytest.raises(PolicyFormatError,match='changed'):read_local(path)


def test_depth_limit_covers_already_seen_shared_nodes():
    leaf=rule_graph.build_operation_node(tuple(ALLOW),0)
    nodes=[leaf]
    for index in range(1,130):
        node=rule_graph.OperationNode(index,tuple(BRANCH));node.parse_raw()
        node.non_terminal.match=nodes[-1];node.non_terminal.unmatch=leaf
        nodes.append(node)
    with pytest.raises(PolicyFormatError,match='depth'):
        with bounded_analysis():profiles._validate_links(nodes)


def test_terminal_c_modifier_payload_stays_inside_literal():
    node=rule_graph.build_operation_node(tuple(ALLOW),0)
    terminal=node.terminal
    terminal.parsed=True;terminal.action_inline=True
    terminal.inline_modifier=SimpleNamespace(policy_op_idx=0)
    terminal.db_modifiers={'inline_modifiers':[{'name':'label'}],'flags_modifiers':[]}
    terminal.ss='x"\n#include "owned"\n'
    rendered=terminal.c_repr()
    assert '\n' not in rendered and '#include' in rendered and '\\012' in rendered


@pytest.mark.parametrize('operation',['read','write'])
def test_fdopen_failure_closes_descriptors(tmp_path,monkeypatch,operation):
    source=tmp_path/'source';source.write_bytes(b'123')
    original_open=os.open;original_close=os.close;opened=[];closed=[]
    def observed_open(*arguments,**keywords):
        value=original_open(*arguments,**keywords);opened.append(value);return value
    def observed_close(descriptor):
        closed.append(descriptor);return original_close(descriptor)
    monkeypatch.setattr(os,'open',observed_open);monkeypatch.setattr(os,'close',observed_close)
    monkeypatch.setattr(os,'fdopen',lambda *a,**kw:(_ for _ in ()).throw(OSError('injected fdopen failure')))
    with pytest.raises(OSError,match='fdopen failure'):
        if operation=='read':read_local(source)
        else:write_exclusive(tmp_path/'report',b'123')
    assert sorted(opened)==sorted(closed)
    for descriptor in opened:
        with pytest.raises(OSError):os.fstat(descriptor)


def test_total_publication_scope_across_multiple_reports(tmp_path):
    from policymosaic.safety import publication_scope
    with publication_scope(5):
        write_exclusive(tmp_path/'first',b'123')
        with pytest.raises(PolicyFormatError,match='total report'):
            write_exclusive(tmp_path/'second',b'456')
    assert (tmp_path/'first').read_bytes()==b'123'
    assert not (tmp_path/'second').exists()
