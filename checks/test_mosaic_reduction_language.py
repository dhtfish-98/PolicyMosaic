"""Independent Boolean path checks for serial contraction and local traversal."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import random
import pytest
from policymosaic import rule_graph
from policymosaic.reduction import operation_paths, validate_graph
from policymosaic.safety import PolicyFormatError


def graph_from(edges, count, negated=()):
    graph=rule_graph.ReducedGraph()
    vertices=[rule_graph.ReducedVertice(value=index,decision=('allow' if index%2 else 'deny'),is_not=index in negated) for index in range(count)]
    for vertex in vertices:graph.add_vertice(vertex)
    for start,end in edges:graph.add_edge_by_vertices(vertices[start],vertices[end])
    graph.set_final_vertices()
    return graph,vertices


def original_actions(edges,count,negated,assignment):
    """Enumerate raw integer adjacency, independent of the reduced graph/AST."""
    children={index:[] for index in range(count)}
    for start,end in edges:children[start].append(end)
    starts=set(range(count))-{end for start,end in edges}
    actions=set()
    def walk(index):
        accepted=not assignment[index] if index in negated else assignment[index]
        if not accepted:return
        if not children[index]:actions.add('allow' if index%2 else 'deny')
        for child in children[index]:walk(child)
    for start in starts:walk(start)
    return actions


def reduced_actions(graph,assignment):
    def condition(vertex):
        if vertex.type=='single':value=assignment[vertex.value]
        elif vertex.type=='require-all':value=all(condition(child) for child in vertex.value)
        elif vertex.type=='require-any':value=any(condition(child) for child in vertex.value)
        else:raise AssertionError(vertex.type)
        return not value if vertex.is_not else value
    actions=set()
    def walk(vertex):
        if not condition(vertex):return
        if vertex in graph.final_vertices:actions.add(vertex.decision)
        for child in graph.get_next_vertices(vertex):walk(child)
    for start in graph.get_start_vertices():walk(start)
    return actions


def verify(edges,count,negated=()):
    graph,vertices=graph_from(edges,count,negated)
    changed=0
    while True:
        count_before=len(graph.vertices)
        for vertex in list(graph.vertices):
            graph.reduce_vertice_single_next(vertex)
            graph.reduce_vertice_single_prev(vertex)
            validate_graph(graph)
        changed+=count_before-len(graph.vertices)
        if count_before==len(graph.vertices):break
    observations=0
    for values in product([False,True],repeat=count):
        assert original_actions(edges,count,set(negated),values)==reduced_actions(graph,values),(edges,values)
        observations+=1
    return observations,changed


@pytest.mark.parametrize('edges,count',[
    ([(0,1),(1,2)],3),
    ([(0,1),(1,2),(2,3)],4),
    ([(0,1),(0,2),(1,3),(3,4),(2,5),(5,6)],7),
    ([(0,2),(1,2),(2,3),(3,4)],5),
    ([(0,1),(1,3),(2,3),(3,4)],5),
])
def test_owned_contracted_boolean_path_languages(edges,count):
    observations,changes=verify(edges,count,range(0,count,2))
    assert observations==2**count and changes>0


def test_seeded_contraction_preserves_all_terminal_path_actions():
    rng=random.Random(864925)
    observations,changes=0,0
    for _ in range(100):
        count=rng.randrange(3,8)
        edges=[(start,end) for start in range(count) for end in range(start+1,count) if rng.random()<0.3]
        negated={index for index in range(count) if rng.random()<0.5}
        checked,changed=verify(edges,count,negated)
        observations+=checked;changes+=changed
    assert observations==4640 and changes>0


@pytest.mark.parametrize('method,selected',[('reduce_vertice_single_prev',2),('reduce_vertice_single_next',0)])
def test_three_node_chain_keeps_edge_and_final_membership(method,selected):
    graph,vertices=graph_from([(0,1),(1,2)],3)
    assert getattr(graph,method)(vertices[selected])
    assert len(graph.vertices)==2 and len(graph.edges)==1
    assert all(edge.start in graph.vertices and edge.end in graph.vertices for edge in graph.edges)
    assert all(vertex in graph.vertices for vertex in graph.final_vertices)


def test_contract_does_not_rewrite_embedded_shared_reference_or_accepting_prefix():
    graph,vertices=graph_from([(0,1)],3)
    vertices[2].type='require-all';vertices[2].value=[vertices[0]]
    assert not graph.reduce_vertice_single_next(vertices[0])
    assert len(graph.vertices)==3
    graph,vertices=graph_from([(0,1)],2)
    graph.final_vertices.append(vertices[0])
    assert not graph.reduce_vertice_single_next(vertices[0])


@pytest.mark.parametrize('kind',['endpoint','final','cycle','duplicate'])
def test_invalid_graph_contract_fails_before_any_mutation(kind):
    graph,vertices=graph_from([(0,1),(1,2)],3)
    if kind=='endpoint':graph.edges[0].start=rule_graph.ReducedVertice(value='outside')
    elif kind=='final':graph.final_vertices.append(rule_graph.ReducedVertice(value='outside'))
    elif kind=='cycle':graph.add_edge_by_vertices(vertices[2],vertices[0])
    else:graph.vertices.append(vertices[2])
    before=(list(graph.vertices),list(graph.edges),list(graph.final_vertices),[(edge.start,edge.end) for edge in graph.edges])
    with pytest.raises(PolicyFormatError):graph.reduce_vertice_single_prev(vertices[2])
    assert before==(list(graph.vertices),list(graph.edges),list(graph.final_vertices),[(edge.start,edge.end) for edge in graph.edges])


def projected(edges,count,finals):
    nodes=[rule_graph.OperationNode(index,(0,)*8) for index in range(count)]
    graph={node:{'type':{'final'} if index in finals else {'normal'},'list':set()} for index,node in enumerate(nodes)}
    for start,end in edges:graph[nodes[start]]['list'].add(nodes[end])
    return graph,nodes


def test_operation_paths_are_finite_local_and_deterministic():
    graph,nodes=projected([(0,1),(0,2),(1,3),(2,3)],4,{3})
    expected=[[0,1,3],[0,2,3]]
    assert [[node.offset for node in path] for path in operation_paths(graph,nodes[0])]==expected
    previous_paths,previous_current=rule_graph.mosaic_paths,rule_graph.mosaic_current_path
    with ThreadPoolExecutor(max_workers=4) as pool:
        answers=list(pool.map(lambda _:rule_graph.get_operation_node_graph_paths(graph,nodes[0]),range(32)))
    assert all([[node.offset for node in path] for path in answer]==expected for answer in answers)
    assert rule_graph.mosaic_paths is previous_paths and rule_graph.mosaic_current_path is previous_current


def test_operation_path_cycle_missing_reference_and_deep_chain():
    graph,nodes=projected([(0,1),(1,0)],2,set())
    with pytest.raises(PolicyFormatError,match='cyclic'):operation_paths(graph,nodes[0])
    del graph[nodes[1]]
    with pytest.raises(PolicyFormatError,match='missing'):operation_paths(graph,nodes[0])
    graph,nodes=projected([(index,index+1) for index in range(129)],130,{129})
    with pytest.raises(PolicyFormatError,match='depth'):operation_paths(graph,nodes[0])


def test_operation_path_expansion_is_bounded(monkeypatch):
    from policymosaic import reduction
    graph,nodes=projected([(0,1),(0,2),(1,3),(2,3)],4,{3})
    monkeypatch.setattr(reduction,'MAX_ITEMS',5)
    with pytest.raises(PolicyFormatError,match='expansion'):operation_paths(graph,nodes[0])


def test_complete_boolean_reduction_preserves_all_raw_path_outcomes():
    rng=random.Random(925286)
    observations=0
    for _ in range(100):
        count=rng.randrange(3,8)
        edges=[(start,end) for start in range(count) for end in range(start+1,count) if rng.random()<0.4]
        negated={index for index in range(count) if rng.random()<0.5}
        graph,vertices=graph_from(edges,count,negated)
        original=[(vertex.type,vertex.value,vertex.is_not,vertex.decision) for vertex in vertices]
        graph.reduce_graph();validate_graph(graph)
        assert graph.edges==[] and len(graph.vertices)<=2
        assert original==[(vertex.type,vertex.value,vertex.is_not,vertex.decision) for vertex in vertices]
        for values in product([False,True],repeat=count):
            assert original_actions(edges,count,negated,values)==reduced_actions(graph,values),(edges,values)
            observations+=1
    assert observations==4440


def test_boolean_reducer_keeps_exact_terminal_modifier_decisions():
    graph,vertices=graph_from([(0,1),(0,2)],3)
    vertices[1].decision='allow (with report)';vertices[2].decision='allow (with no-report)'
    graph.reduce_graph()
    assert {vertex.decision for vertex in graph.vertices}=={'allow (with report)','allow (with no-report)'}


def test_boolean_reducer_incomplete_outcome_does_not_mutate_graph():
    graph,vertices=graph_from([(0,1)],2)
    vertices[1].decision=None
    before=(list(graph.vertices),list(graph.edges),list(graph.final_vertices))
    with pytest.raises(PolicyFormatError,match='terminal decision'):graph.reduce_graph()
    assert before==(list(graph.vertices),list(graph.edges),list(graph.final_vertices))


def test_shared_expression_depth_and_cycle_are_not_hidden_by_seen_nodes():
    graph,vertices=graph_from([(0,1)],3)
    shared='leaf'
    for _ in range(50):shared=[shared]
    longest=shared
    for _ in range(90):longest=[longest]
    vertices[2].value=[shared,longest]
    with pytest.raises(PolicyFormatError,match='embedded'):graph.reduce_graph()
    vertices[2].value=[];vertices[2].value.append(vertices[2].value)
    with pytest.raises(PolicyFormatError,match='cyclic embedded'):graph.reduce_vertice_single_next(vertices[0])
