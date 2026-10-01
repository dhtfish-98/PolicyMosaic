"""Known-answer cases for offline sandbox formats, without external devices."""
import argparse as mosaic_argparse
import io as mosaic_io
import struct as mosaic_struct
import pytest as mosaic_pytest
from policymosaic import profile_decoder as mosaic_profiles
from policymosaic import regex_bytecode as mosaic_regex
from policymosaic import string_bytecode as mosaic_strings
from policymosaic import rule_graph as mosaic_nodes
from policymosaic import firmware_helper as mosaic_helper
from policymosaic import filter_catalog as mosaic_filters
import policymosaic_boundary as mosaic_boundary


@mosaic_pytest.mark.parametrize('mosaic_opcode,mosaic_wire,mosaic_answer', [
    (0x02,b'.',{'pos':-6,'type':'character','value':'[.]'}),
    (0x02,b'x',{'pos':-6,'type':'character','value':'x'}),
    (0x19,b'',{'pos':-6,'type':'character','value':'^'}),
    (0x29,b'',{'pos':-6,'type':'character','value':'$'}),
    (0x09,b'',{'pos':-6,'type':'character','value':'.'}),
    (0x2f,b'\x34\x12',{'pos':-6,'type':'jump_forward','value':0x1234}),
    (0x0a,b'\x78\x56',{'pos':-6,'type':'jump_backward','value':0x5678}),
    (0x25,b'',{'pos':-6,'type':'end','value':0}),
])
def test_mosaic_regex_known_answers(mosaic_opcode,mosaic_wire,mosaic_answer):
    mosaic_records=[]
    mosaic_regex.mosaic_parse(bytes([mosaic_opcode])+mosaic_wire,0,mosaic_records)
    assert mosaic_records==[mosaic_answer]


@mosaic_pytest.mark.parametrize('mosaic_text',['','a','.','alpha','/tmp/example','场景','a'*32])
def test_mosaic_literal_bytecode(mosaic_text):
    mosaic_bytes=mosaic_text.encode()
    mosaic_wire=bytes([0x3f+len(mosaic_bytes)])+mosaic_bytes+b'\x0a'
    assert mosaic_strings.mosaic_SandboxString().mosaic_parse_byte_string(mosaic_wire,[])==[mosaic_text]


@mosaic_pytest.mark.parametrize('mosaic_size',range(16))
def test_mosaic_truncated_header_rejected(mosaic_size):
    with mosaic_pytest.raises(mosaic_struct.error):
        mosaic_profiles.mosaic_parse_profile(mosaic_io.BytesIO(b'\0'*mosaic_size),mosaic_argparse.Namespace(release='17'))


def test_mosaic_header_offsets_and_display_labels():
    mosaic_wire=mosaic_struct.pack('<HHBBBxHHHH',0,2,3,1,2,4,1,1,0)
    mosaic_data=mosaic_profiles.mosaic_parse_profile(mosaic_io.BytesIO(mosaic_wire),mosaic_argparse.Namespace(release='17'))
    assert mosaic_data.mosaic_header_size==14
    assert mosaic_data.mosaic_operation_nodes_offset==72
    assert mosaic_data.mosaic_base_addr==88
    assert 'op_nodes_count: 0x2' in repr(mosaic_data)
    assert mosaic_data.op_nodes_count==mosaic_data.mosaic_op_nodes_count==2


@mosaic_pytest.mark.parametrize('mosaic_kind,mosaic_expected',[(0,'allow'),(1,'deny'),(2,'unknown')])
def test_mosaic_terminal_actions(mosaic_kind,mosaic_expected):
    mosaic_terminal=mosaic_nodes.mosaic_TerminalNode()
    mosaic_terminal.mosaic_type=mosaic_kind
    assert str(mosaic_terminal)==mosaic_expected


@mosaic_pytest.mark.parametrize('mosaic_output,mosaic_path',[
    ('Created /tmp/kernel','/tmp/kernel'),
    ('kernelcache already exists /tmp/kernel','/tmp/kernel'),
    ('progress\nCreated ./kernel','kernel'),
])
def test_mosaic_firmware_helper_path_parser(mosaic_output,mosaic_path):
    assert str(mosaic_helper.mosaic_ipsw_get_out_path(mosaic_output))==mosaic_path


def test_mosaic_packaged_resource_catalog():
    assert mosaic_filters.mosaic_Filters.mosaic_filters
    assert mosaic_boundary.resource('filters.json').endswith('policymosaic/data/filters.json')


def test_mosaic_helper_invokes_current_module():
    mosaic_invocation=mosaic_boundary.decoder_invocation('--release','17','profile.bin')
    assert mosaic_invocation[1:]==['-m','policymosaic.profile_decoder','--release','17','profile.bin']
