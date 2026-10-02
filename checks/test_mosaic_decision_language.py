"""Decisions and emitted forms checked against independent raw-record traversal."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import io
import random
import re
import struct
import pytest
from policymosaic import rule_graph
from policymosaic.decision_graph import compile_decisions,evaluate_condition
from policymosaic.safety import PolicyFormatError


ALLOW=bytes((1,0,0,0,0,0,0,0));DENY=bytes((1,1,0,0,0,0,0,0))


def branch(argument,matched,unmatched,filter_id=200):
    return struct.pack('<BBHHH',0,filter_id,argument,matched,unmatched)


def nodes(records):
    result=rule_graph.build_operation_nodes(io.BytesIO(b''.join(records)),len(records))
    for node in result:
        if node.non_terminal is not None:
            node.non_terminal.filter='predicate'
            node.non_terminal.argument=str(node.non_terminal.argument_id)
    return result


def raw_decision(records,root,assignment):
    """Follow branch offsets in bytes, using no graph compiler or expression AST."""
    visited=set()
    while records[root][0]==0:
        assert root not in visited
        visited.add(root)
        _,_,argument,matched,unmatched=struct.unpack('<BBHHH',records[root])
        root=matched if assignment[argument] else unmatched
    return 'deny' if records[root][1]&1 else 'allow'


def parse_forms(text):
    tokens=re.findall(r'\(|\)|[^\s()]+',text)
    stack,forms=[],[]
    for token in tokens:
        if token=='(':
            form=[]
            if stack:stack[-1].append(form)
            else:forms.append(form)
            stack.append(form)
        elif token==')':
            assert stack
            stack.pop()
        else:
            assert stack
            stack[-1].append(token)
    assert not stack
    return forms


def form_truth(form,assignment):
    name,*arguments=form
    if name=='predicate':return assignment[int(arguments[0])]
    if name=='require-not':return not form_truth(arguments[0],assignment)
    if name=='require-all':return all(form_truth(value,assignment) for value in arguments)
    if name=='require-any':return any(form_truth(value,assignment) for value in arguments)
    raise AssertionError(form)


def verify(records,root,default=0):
    graph=nodes(records)
    raw_before=[(node.raw,node.non_terminal.match if node.non_terminal else None,node.non_terminal.unmatch if node.non_terminal else None,node.non_terminal.argument if node.non_terminal else None) for node in graph]
    plan=compile_decisions(graph[root],graph[default]);assert plan is not None
    output=io.StringIO();plan.emit('file-read*',output);forms=parse_forms(output.getvalue())
    variables=sorted({struct.unpack('<H',record[2:4])[0] for record in records if record[0]==0})
    observations=0
    for values in product([False,True],repeat=len(variables)):
        assignment=dict(zip(variables,values))
        expected=raw_decision(records,root,assignment)
        symbolic={key:assignment[key[1]] for key in plan.predicates}
        chosen=[rule for rule in plan.rules if evaluate_condition(rule.condition,symbolic)]
        assert len(chosen)==1 and chosen[0].outcome.action==expected,(records,assignment,chosen)
        actual=[form[0] for form in forms if not form[2:] or all(form_truth(item,assignment) for item in form[2:])]
        assert len(actual)<=1,(records,assignment,output.getvalue())
        reported=actual[0] if actual else ('deny' if records[default][1]&1 else 'allow')
        assert reported==expected,(records,assignment,output.getvalue())
        observations+=1
    raw_after=[(node.raw,node.non_terminal.match if node.non_terminal else None,node.non_terminal.unmatch if node.non_terminal else None,node.non_terminal.argument if node.non_terminal else None) for node in graph]
    assert raw_after==raw_before
    return observations


@pytest.mark.parametrize('records,root,default',[
    ([ALLOW,DENY,branch(2,0,1)],2,0),
    ([ALLOW,DENY,branch(2,1,0)],2,0),
    ([ALLOW,DENY,branch(2,0,0)],2,1),
    ([ALLOW,DENY,branch(2,1,1)],2,0),
    ([ALLOW,DENY,branch(2,0,1),branch(3,2,0),branch(4,2,3)],4,0),
    ([ALLOW,DENY,branch(2,0,1),branch(2,1,2)],3,0),
    ([ALLOW,DENY,branch(2,0,1),branch(2,2,1)],3,1),
])
def test_owned_raw_decision_languages(records,root,default):
    assert verify(records,root,default)>=2


def test_seeded_raw_graph_and_emitted_form_decisions():
    rng=random.Random(483175)
    observations=0
    for _ in range(100):
        records=[ALLOW,DENY]
        for index in range(2,rng.randrange(3,11)):
            records.append(branch(index,rng.randrange(index),rng.randrange(index)))
        observations+=verify(records,len(records)-1,rng.randrange(2))
    assert observations==6112


def test_same_action_modifier_outcome_is_preserved_in_report():
    records=[ALLOW,bytes((1,4,0,0,0,0,0,0)),branch(2,1,0)]
    graph=nodes(records)
    graph[1].terminal.db_modifiers['flags_modifiers']=graph[1].terminal.get_modifiers_by_flag(4)
    plan=compile_decisions(graph[2],graph[0]);assert plan is not None
    output=io.StringIO();plan.emit('file-read*',output)
    assert '(allow file-read* (with report)' in output.getvalue()
    assert '(predicate 2)' in output.getvalue()
    for value in [False,True]:
        chosen=[rule.outcome for rule in plan.rules if evaluate_condition(rule.condition,{key:value for key in plan.predicates})]
        assert len(chosen)==1
        assert chosen[0].action=='allow'
        assert chosen[0].modifiers==(' (with report)' if value else '')


@pytest.mark.parametrize('filter_id',[30,31,32,160])
def test_contextual_entitlement_path_is_not_mislabeled_as_ordinary(filter_id):
    graph=nodes([ALLOW,DENY,branch(2,0,1,filter_id)])
    assert compile_decisions(graph[2],graph[0]) is None


def test_inline_policy_reference_is_not_mislabeled_as_an_ordinary_outcome():
    graph=nodes([ALLOW,bytes((1,0,0,128,1,1,0,0))])
    assert compile_decisions(graph[1],graph[0]) is None
    assert compile_decisions(graph[0],graph[1]) is None


def test_missing_cycle_reference_and_shared_node_depth_are_incomplete():
    graph=nodes([ALLOW,DENY,branch(2,2,0)])
    with pytest.raises(PolicyFormatError,match='cyclic'):compile_decisions(graph[2],graph[0])
    graph[2].non_terminal.match=None
    with pytest.raises(PolicyFormatError,match='missing'):compile_decisions(graph[2],graph[0])
    records=[ALLOW,DENY]
    for index in range(2,132):records.append(branch(index,index-1,0))
    graph=nodes(records)
    with pytest.raises(PolicyFormatError,match='depth'):compile_decisions(graph[-1],graph[0])


def test_parallel_decision_compilation_does_not_mutate_shared_nodes():
    graph=nodes([ALLOW,DENY,branch(2,0,1),branch(3,2,0)])
    original=(graph[3].non_terminal.match,graph[3].non_terminal.unmatch,graph[2].non_terminal.argument)
    def inspect(default):
        plan=compile_decisions(graph[3],graph[default]);output=io.StringIO();plan.emit('file-read*',output)
        return output.getvalue()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(inspect,[0,1]*16))
    assert len(set(results[::2]))==1 and len(set(results[1::2]))==1
    assert (graph[3].non_terminal.match,graph[3].non_terminal.unmatch,graph[2].non_terminal.argument)==original


@pytest.mark.parametrize('argument',[7,[7],{'a':'b'}])
def test_incomplete_predicate_presentation_is_explicit(argument):
    graph=nodes([ALLOW,DENY,branch(2,1,0)])
    graph[2].non_terminal.argument=argument
    with pytest.raises(PolicyFormatError,match='predicate argument'):
        compile_decisions(graph[2],graph[0])


def test_unconverted_predicate_is_not_emitted_as_raw_record():
    graph=nodes([ALLOW,DENY,branch(2,1,0)])
    graph[2].non_terminal.filter=None
    with pytest.raises(PolicyFormatError,match='not been converted'):
        compile_decisions(graph[2],graph[0])


def test_catalog_suppressed_builtin_uses_its_compatibility_path():
    graph=nodes([ALLOW,DENY,branch(2,1,0,129)])
    graph[2].non_terminal.argument='###$$$***'
    assert compile_decisions(graph[2],graph[0]) is None


def test_literal_data_matching_legacy_marker_is_not_a_contextual_flag():
    graph=nodes([ALLOW,DENY,branch(2,1,0,1)])
    graph[2].non_terminal.filter='literal'
    graph[2].non_terminal.argument=['###$$$***']
    assert compile_decisions(graph[2],graph[0]) is not None


def test_decision_interning_and_expansion_limits(monkeypatch):
    from policymosaic import decision_graph
    graph=nodes([ALLOW,DENY,branch(2,1,0)])
    monkeypatch.setattr(decision_graph,'MAX_ITEMS',3)
    with pytest.raises(PolicyFormatError,match='count/depth/expansion'):
        compile_decisions(graph[2],graph[0])
    monkeypatch.setattr(decision_graph,'MAX_ITEMS',65536)
    monkeypatch.setattr(decision_graph,'OUTPUT_BYTES',100)
    graph[2].non_terminal.argument='x'*101
    with pytest.raises(PolicyFormatError,match='exceeds limit'):
        compile_decisions(graph[2],graph[0])


@pytest.mark.parametrize('default,leaf,expected',[(DENY,ALLOW,b'(allow file-read*)'),(ALLOW,DENY,b'(deny file-read* (with no-report))')])
def test_actual_cli_same_terminal_branches_are_unconditional(tmp_path,default,leaf,expected):
    from pathlib import Path
    import os,subprocess,sys
    from test_mosaic_safety import fixture
    root=Path(__file__).resolve().parents[1]
    data=fixture((default,leaf,struct.pack('<BBHHH',0,13,6,1,1)),(0,2))
    source=tmp_path/'input.bin';source.write_bytes(data)
    ops=tmp_path/'operations';ops.write_text('default\nfile-read*\n')
    command=[sys.executable,'-m','policymosaic.profile_decoder','-r','17','-o',str(ops),'-d',str(tmp_path),str(source)]
    result=subprocess.run(command,env=dict(os.environ,PYTHONPATH=str(root/'src')),capture_output=True,timeout=5)
    assert result.returncode==0,result.stderr
    report=(tmp_path/'input.sb').read_bytes()
    assert expected+b'\n' in report
    assert source.read_bytes()==data
    assert b'socket-type' not in report


def test_legacy_single_next_path_no_longer_uses_an_undefined_variable():
    graph=rule_graph.ReducedGraph()
    first=rule_graph.ReducedVertice(value='left',decision='allow')
    last=rule_graph.ReducedVertice(value='right',decision='allow')
    graph.add_vertice(first);graph.add_vertice(last);graph.add_edge_by_vertices(first,last)
    graph.set_final_vertices();graph.reduce_vertice_single_next(first)
    assert len(graph.vertices)==1
    assert graph.vertices[0].type=='require-all'
    assert graph.vertices[0].value==[first,last]


def test_legacy_negative_entitlement_no_longer_indexes_dict_keys():
    graph=nodes([ALLOW,DENY,branch(2,0,1,30),branch(3,0,1,31)])
    graph[2].non_terminal.filter='require-entitlement';graph[2].non_terminal.argument=['owned-permission']
    graph[3].non_terminal.filter='entitlement-value';graph[3].non_terminal.argument='#t'
    projection={graph[2]:{'decision':'deny','not':True,'list':set(),'type':{'start'}},graph[3]:{'decision':'deny','not':False,'list':set(),'type':{'start'}}}
    reduced=rule_graph.reduce_operation_node_graph(projection)
    assert isinstance(reduced,rule_graph.ReducedGraph)
