"""Owned automata checked against an independent configuration-set interpreter."""
from itertools import product
import random
import re
import struct
from types import SimpleNamespace
import pytest
from policymosaic import regex_graph, filter_decoder
from policymosaic.safety import PolicyFormatError


def records(*instructions):
    return [{'pos':index,'type':kind,'value':value} for index,(kind,value) in enumerate(instructions)]


def accepts(program, word):
    """Execute record transitions; do not use regex construction/elimination."""
    positions = {item['pos']:index for index,item in enumerate(program)}
    todo, visited = [(0,0)], set()
    while todo:
        state, offset = todo.pop()
        if (state,offset) in visited or state >= len(program): continue
        visited.add((state,offset))
        item = program[state]; kind, value = item['type'], item['value']
        if kind == 'end':
            if offset == len(word): return True
        elif kind in ('jump_forward','jump_backward'):
            target = positions.get(value, positions.get(value + 1))
            todo.append((target,offset))
            if kind == 'jump_forward': todo.append((state+1,offset))
        elif value == '^':
            if offset == 0: todo.append((state+1,offset))
        elif value == '$':
            if offset == len(word): todo.append((state+1,offset))
        elif offset < len(word):
            character = word[offset]
            allowed = character == value or value == '.' or value == '[ab]' and character in 'ab' or value == '[^a]' and character != 'a'
            if allowed: todo.append((state+1,offset+1))
    return False


def compile_graph(program):
    graph = regex_graph.Graph()
    graph.fill_from_regex_list(program)
    graph.reduce();graph.convert_to_canonical();graph.simplify();graph.combine_start_end_nodes()
    return graph.regex


def compile_wire(program):
    """Assemble owned records, resolving labels to byte offsets."""
    offsets, position = {}, 0
    fixed = {'^':b'\x19','$':b'\x29','.':b'\x09','[ab]':b'\x1bab','[^a]':b'\x1bb`'}
    fragments=[]
    for item in program:
        offsets[item['pos']]=position
        kind, value = item['type'],item['value']
        fragment = b'\x25\0' if kind=='end' else b'\0'*3 if kind.startswith('jump_') else fixed.get(value,bytes((2,ord(value))) if len(value)==1 else b'')
        assert fragment
        fragments.append(fragment);position+=len(fragment)
    for index,item in enumerate(program):
        if item['type'].startswith('jump_'):
            fragments[index]=bytes((47 if item['type']=='jump_forward' else 10,))+struct.pack('<H',offsets[item['value']])
    return regex_graph.parse_regex(b'\0'*6+b''.join(fragments))


def check_language(program, alphabet='ab', depth=5):
    variants = [compile_graph(program),compile_wire(program)]
    patterns = [[re.compile(expression) for expression in rendered] for rendered in variants]
    count = 0
    for length in range(depth+1):
        for letters in product(alphabet,repeat=length):
            word = ''.join(letters)
            expected = accepts(program,word)
            for rendered,compiled in zip(variants,patterns):
                actual = any(pattern.fullmatch(word) is not None for pattern in compiled)
                assert actual == expected,(program,rendered,word,expected)
                count += 1
    return count


@pytest.mark.parametrize('program',[
    records(('character','a'),('end',0)),
    records(('jump_forward',2),('character','a'),('end',0)),
    records(('jump_forward',4),('character','a'),('jump_backward',0),('end',0),('end',0)),
    records(('character','a'),('jump_forward',3),('jump_backward',0),('end',0)),
    records(('jump_forward',3),('character','a'),('jump_backward',4),('character','b'),('end',0)),
    records(('jump_forward',4),('character','a'),('jump_backward',6),('end',0),('character','b'),('jump_backward',6),('character','a'),('end',0)),
    records(('jump_forward',3),('jump_backward',0),('end',0),('character','a'),('end',0)),
    records(('character','^'),('class','[ab]'),('character','$'),('end',0)),
    records(('class_exclude','[^a]'),('character','.'),('end',0)),
    records(('jump_forward',3),('character','^'),('jump_backward',0),('end',0)),
    records(('jump_forward',3),('character','$'),('jump_backward',0),('end',0)),
    records(('jump_forward',4),('character','a'),('jump_forward',4),('jump_backward',0),('character','b'),('jump_forward',0),('end',0)),
])
def test_owned_regex_languages(program):
    assert check_language(program)==126


def test_seeded_automata_language_property():
    rng=random.Random(910231)
    observations = 0
    for _ in range(100):
        count = rng.randrange(2,9)
        program=[]
        for state in range(count-1):
            kind = rng.choice(['character','character','jump_forward','jump_backward'])
            value = rng.choice('ab') if kind=='character' else rng.randrange(count)
            program.append({'pos':state,'type':kind,'value':value})
        program.append({'pos':count-1,'type':'end','value':0})
        observations += check_language(program)
    assert observations==12600


@pytest.mark.parametrize('byte',range(256))
def test_literal_opcode_is_data_even_for_regex_operators(byte):
    rendered=regex_graph.parse_regex(b'\0'*6+bytes((2,byte,0x25,0)))
    assert len(rendered)==1
    pattern=re.compile(rendered[0])
    assert pattern.fullmatch(chr(byte)) is not None
    assert pattern.fullmatch('') is None
    assert pattern.fullmatch(chr((byte+1)%256)) is None
    assert pattern.fullmatch(chr(byte)*2) is None


def test_parallel_self_loops_are_unioned_and_nullable_paths_survive():
    graph=regex_graph.Graph()
    graph.canon_graph_dict={-1:[('',0)],0:[('a',0),('b',0)]}
    graph.end_states=[0]
    graph.combine_start_end_nodes()
    pattern=re.compile(graph.regex[0])
    assert all(pattern.fullmatch(word) is not None for word in ['', 'a','b','abba'])
    assert pattern.fullmatch('c') is None


def test_class_alternatives_keep_precedence_when_concatenated():
    graph=regex_graph.Graph()
    graph.canon_graph_dict={-1:[('[a]|[b]',0)],0:[('c',1)],1:[]}
    graph.end_states=[1]
    graph.simplify();graph.combine_start_end_nodes()
    pattern=re.compile(graph.regex[0])
    assert pattern.fullmatch('ac') and pattern.fullmatch('bc')
    assert not pattern.fullmatch('a') and not pattern.fullmatch('b')


def test_empty_language_is_not_silently_published_as_an_empty_filter():
    program=records(('jump_backward',0),('end',0))
    assert compile_graph(program)==[]
    context=SimpleNamespace(base_addr=0,global_vars=[],regex_list=[[]],sb_ops=[])
    with filter_decoder._conversion_context(context,True):
        with pytest.raises(PolicyFormatError,match='no representable accepting path'):
            filter_decoder.get_filter_arg_regex_by_id(None,0)


@pytest.mark.parametrize('program',[
    [{'pos':0,'type':'character','value':'a'}],
    [{'pos':0,'type':'unknown','value':0}],
    [{'pos':0,'type':[],'value':0}],
    [{'pos':0,'type':'end','value':0},{'pos':0,'type':'end','value':0}],
    [{'pos':0,'type':'jump_forward','value':True},{'pos':1,'type':'end','value':0}],
])
def test_record_validation_is_explicit(program):
    with pytest.raises(PolicyFormatError):regex_graph.Graph().fill_from_regex_list(program)


@pytest.mark.parametrize('lower,upper',[(0,0),(1,31),(32,32),(34,34),(45,45),(46,46),(91,91),(92,92),(93,93),(94,94),(97,122),(127,127),(128,255),(0,255)])
def test_real_character_class_byte_intervals(lower,upper):
    patterns=[re.compile(text) for text in regex_graph.parse_regex(b'\0'*6+bytes((0x1b,lower,upper,0x25,0)))]
    for byte in range(256):
        assert any(pattern.fullmatch(chr(byte)) is not None for pattern in patterns)==(lower<=byte<=upper)


@pytest.mark.parametrize('byte',[1,34,45,91,92,93,94,127,254])
def test_real_excluded_character_class_byte_intervals(byte):
    patterns=[re.compile(text) for text in regex_graph.parse_regex(b'\0'*6+bytes((0x1b,byte+1,byte-1,0x25,0)))]
    for candidate in range(256):
        assert any(pattern.fullmatch(chr(candidate)) is not None for pattern in patterns)==(candidate!=byte)


def test_descending_character_class_interval_is_incomplete():
    with pytest.raises(PolicyFormatError,match='character-class interval'):
        regex_graph.parse_regex(b'\0'*6+bytes((0x2b,100,97,97,122,0x25,0)))


def test_regex_quoted_presentation_round_trips_data():
    import json
    expression='a"\\.\n\0b'
    context=SimpleNamespace(base_addr=0,global_vars=[],regex_list=[[expression]],sb_ops=[])
    with filter_decoder._conversion_context(context,True):
        presentation=filter_decoder.get_filter_arg_regex_by_id(None,0)
    assert presentation.startswith('#"')
    assert '\n' not in presentation and '\0' not in presentation
    assert json.loads(presentation[1:])==expression


def test_end_marker_padding_is_checked():
    with pytest.raises(PolicyFormatError,match='end marker'):
        regex_graph.parse_regex(b'\0'*6+b'\x25')


@pytest.mark.parametrize('names',[('0','0'),('-1','0'),('4096','0'),('x','0')])
def test_invalid_direct_node_indices_are_incomplete(names):
    first=regex_graph.Node(names[0]);first.set_type_character();first.set_value('a')
    last=regex_graph.Node(names[1]);last.set_type_end()
    graph=regex_graph.Graph();graph.graph_dict={first:[last],last:[]}
    with pytest.raises(PolicyFormatError,match='node index'):graph.reduce()


def test_parallel_regex_calls_keep_distinct_owned_state():
    from concurrent.futures import ThreadPoolExecutor
    def inspect(byte):
        expressions=regex_graph.parse_regex(b'\0'*6+bytes((2,byte,0x25,0)))
        return len(expressions)==1 and re.fullmatch(expressions[0],chr(byte)) is not None and re.fullmatch(expressions[0],'') is None
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert all(pool.map(inspect,range(256)))


@pytest.mark.parametrize('canonical',[
    {-1:[('a',0)]},
    {-1:[('a',True)],1:[]},
    {-1:[(4,0)],0:[]},
    {-1:[('a',0,1)],0:[]},
    {-1:[],4096:[]},
])
def test_invalid_canonical_edges_are_explicit(canonical):
    graph=regex_graph.Graph();graph.canon_graph_dict=canonical
    with pytest.raises(PolicyFormatError):graph.combine_start_end_nodes()


def test_record_count_limit_is_checked_before_graph_allocation():
    program=[{'pos':index,'type':'end','value':0} for index in range(4097)]
    with pytest.raises(PolicyFormatError,match='over-limit'):regex_graph.Graph().fill_from_regex_list(program)


def test_actual_regex_collection_cli_bounds_and_input_immutability(tmp_path):
    from pathlib import Path
    import ast,os,subprocess,sys
    root=Path(__file__).resolve().parents[1]
    wire=b'\0'*6+b'\x02+\x25\0'
    data=struct.pack('<HH',1,len(wire))+wire
    source=tmp_path/'regexes';source.write_bytes(data)
    env=dict(os.environ,PYTHONPATH=str(root/'src'))
    command=[sys.executable,'-m','policymosaic.regex_graph',str(source)]
    result=subprocess.run(command,env=env,capture_output=True,timeout=4)
    assert result.returncode==0,result.stderr
    expressions=ast.literal_eval(result.stdout.decode())
    assert len(expressions)==1 and re.fullmatch(expressions[0],'+')
    assert source.read_bytes()==data
    for bad in [struct.pack('<H',4097),data+b'x',b'\0']:
        source.write_bytes(bad)
        result=subprocess.run(command,env=env,capture_output=True,timeout=4)
        assert result.returncode==2 and b'Traceback' not in result.stderr
        assert source.read_bytes()==bad
