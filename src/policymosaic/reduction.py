"""Local graph traversal and serial contraction for attributed rule helpers.

These operations preserve finite Boolean paths. They do not infer entitlement
binding or inline-policy semantics, which require their own interpretation.
"""
from policymosaic.safety import (PolicyFormatError, MAX_NODES, MAX_ITEMS,
    MAX_DEPTH, OUTPUT_BYTES, analysis_guard, analysis_step)


@analysis_guard
def operation_paths(graph, start):
    """Enumerate explicit final paths without shared module state or recursion."""
    if not isinstance(graph, dict) or len(graph) > MAX_NODES or start not in graph:
        raise PolicyFormatError('invalid operation path graph')
    paths, pending, slots = [], [(start, ())], 0
    while pending:
        analysis_step()
        node, prefix = pending.pop()
        if node not in graph or not isinstance(graph[node], dict):
            raise PolicyFormatError('missing operation path node')
        if node in prefix: raise PolicyFormatError('cyclic operation path graph')
        path = prefix + (node,)
        if len(path) > MAX_DEPTH: raise PolicyFormatError('operation path depth exceeds limit')
        metadata = graph[node]
        kinds, children = metadata.get('type'), metadata.get('list')
        if not isinstance(kinds, (set, frozenset)) or not isinstance(children, (set, frozenset, list, tuple)):
            raise PolicyFormatError('invalid operation path metadata')
        if 'final' in kinds:
            slots += len(path)
            if len(paths) >= MAX_ITEMS or slots > MAX_ITEMS:
                raise PolicyFormatError('operation path expansion exceeds limit')
            paths.append(list(path))
        else:
            if len(children) > MAX_NODES: raise PolicyFormatError('operation path branching exceeds limit')
            if any(child not in graph for child in children):
                raise PolicyFormatError('missing operation path node')
            # Ordering is explicit where node records provide their canonical index.
            ordered = sorted(children, key=lambda child: child.offset)
            pending.extend((child, path) for child in reversed(ordered))
            if len(pending) > MAX_ITEMS: raise PolicyFormatError('operation path work queue exceeds limit')
    return paths


@analysis_guard
def validate_graph(graph):
    """Check identity membership, finite references and DAG depth before mutation."""
    vertices, edges, finals = list(graph.vertices), list(graph.edges), list(graph.final_vertices)
    members = {id(vertex): vertex for vertex in vertices}
    if len(members) != len(vertices) or len(vertices) > MAX_NODES or len(edges) > MAX_ITEMS:
        raise PolicyFormatError('invalid reduced graph membership or size')
    if any(id(vertex) not in members for vertex in finals):
        raise PolicyFormatError('reduced final vertex is outside graph')
    following = {id(vertex): [] for vertex in vertices}
    for edge in edges:
        analysis_step()
        if id(edge.start) not in members or id(edge.end) not in members:
            raise PolicyFormatError('reduced edge endpoint is outside graph')
        following[id(edge.start)].append(id(edge.end))
    completed, active, height = set(), set(), {}
    for vertex in vertices:
        pending = [(id(vertex), False)]
        while pending:
            analysis_step()
            identity, leaving = pending.pop()
            if leaving:
                height[identity] = 1 + max((height[child] for child in following[identity]), default=0)
                if height[identity] > MAX_DEPTH: raise PolicyFormatError('reduced graph depth exceeds limit')
                active.remove(identity); completed.add(identity)
            elif identity in active:
                raise PolicyFormatError('cyclic reduced graph')
            elif identity not in completed:
                active.add(identity); pending.append((identity, True))
                pending.extend((child, False) for child in reversed(following[identity]))
    return vertices, edges, finals


def _contains_reference(vertex, targets):
    """Embedded shared references prevent contraction; they are not rewritten."""
    pending, visited, active, heights = [(vertex.value, False)], set(), set(), {}
    while pending:
        analysis_step()
        value, leaving = pending.pop()
        if id(value) in targets: return True
        children = list(value) if isinstance(value, (list, tuple)) else [value.value] if hasattr(value, 'value') else []
        if leaving:
            heights[id(value)] = 1 + max((heights[id(child)] for child in children), default=0)
            if heights[id(value)] > MAX_DEPTH:
                raise PolicyFormatError('embedded reduced expression exceeds limit')
            active.remove(id(value)); visited.add(id(value)); continue
        if id(value) in active: raise PolicyFormatError('cyclic embedded reduced expression')
        if len(visited) + len(active) >= MAX_ITEMS or len(children) > MAX_ITEMS:
            raise PolicyFormatError('embedded reduced expression exceeds limit')
        if id(value) in visited: continue
        active.add(id(value));pending.append((value, True))
        pending.extend((child, False) for child in reversed(children))
    return False


@analysis_guard
def contract_serial(graph, first, last, vertex_type, edge_type):
    """Replace an exclusive first -> last chain and atomically publish membership."""
    # A reduction loop may pass a vertex removed by an earlier contraction.
    if first not in graph.vertices or last not in graph.vertices: return False
    vertices, edges, finals = validate_graph(graph)
    for vertex in vertices: _contains_reference(vertex, set())
    if first is last: raise PolicyFormatError('cannot contract a self edge')
    successors = {id(edge.end) for edge in edges if edge.start is first}
    predecessors = {id(edge.start) for edge in edges if edge.end is last}
    if successors != {id(last)} or predecessors != {id(first)}: return False
    # An explicit accepting prefix has different semantics from a full chain.
    if first in finals: return False
    targets = {id(first), id(last)}
    if any(_contains_reference(vertex, targets) for vertex in vertices if vertex not in (first, last)):
        return False
    children = []
    for vertex in (first, last):
        if vertex.is_type_require_all() and not vertex.is_not:
            if not isinstance(vertex.value, list): raise PolicyFormatError('incomplete reduced conjunction')
            children.extend(vertex.value)
        else: children.append(vertex)
    if len(children) > MAX_ITEMS: raise PolicyFormatError('reduced conjunction exceeds limit')
    replacement = vertex_type('require-all', children, last.decision)
    new_edges, seen = [], set()
    for edge in edges:
        analysis_step()
        if edge.start is first and edge.end is last: continue
        start = replacement if edge.start is last else edge.start
        end = replacement if edge.end is first else edge.end
        identity = id(start), id(end)
        if identity not in seen:
            new_edges.append(edge_type(start, end)); seen.add(identity)
    new_vertices = [replacement if vertex is first else vertex for vertex in vertices if vertex is not last]
    new_finals = [replacement if vertex is last else vertex for vertex in finals]
    # Validate the candidate before touching the caller's graph.
    candidate = type('Candidate', (), {'vertices':new_vertices,'edges':new_edges,'final_vertices':new_finals})()
    validate_graph(candidate)
    graph.vertices, graph.edges, graph.final_vertices = new_vertices, new_edges, new_finals
    graph.reduce_changes_occurred = True
    return True


@analysis_guard
def reduce_boolean_graph(graph, vertex_type):
    """Compile all accepting Boolean paths, grouping exact final decision strings.

    Each input vertex is an opaque predicate expression. Contextual binding
    interpretation and presentation remain responsibilities of their callers.
    The caller's graph is replaced only after successful finite compilation.
    """
    vertices, edges, _ = validate_graph(graph)
    for vertex in vertices: _contains_reference(vertex, set())
    following = {id(vertex): [] for vertex in vertices}
    for edge in edges: following[id(edge.start)].append(edge.end)
    incoming = {id(edge.end) for edge in edges}
    starts = [vertex for vertex in vertices if id(vertex) not in incoming]
    postorder, visited = [], set()
    for vertex in starts:
        pending = [(vertex, False)]
        while pending:
            analysis_step()
            current, leaving = pending.pop()
            if id(current) in visited: continue
            if leaving:
                postorder.append(current); visited.add(id(current))
            else:
                pending.append((current, True))
                pending.extend((child, False) for child in reversed(following[id(current)]))
    interned, generated, depths = {}, set(), {}

    def combine(kind, children):
        combined, present = [], set()
        for child in children:
            analysis_step()
            values = child.value if id(child) in generated and child.type == kind else [child]
            for value in values:
                analysis_step()
                if id(value) not in present:
                    combined.append(value); present.add(id(value))
        if len(combined) == 1: return combined[0]
        signature = kind, tuple(id(child) for child in combined)
        if signature in interned: return interned[signature]
        depth = 1 + max((depths.get(id(child), 1) for child in combined), default=0)
        if len(combined) > MAX_ITEMS or len(interned) >= MAX_ITEMS or depth > MAX_DEPTH:
            raise PolicyFormatError('reduced Boolean expression exceeds limit')
        expression = vertex_type(kind, combined, None)
        interned[signature] = expression; generated.add(id(expression)); depths[id(expression)] = depth
        return expression

    decisions, slots = {}, 0
    for vertex in postorder:
        analysis_step()
        children = following[id(vertex)]
        if not children:
            if not isinstance(vertex.decision, str) or not vertex.decision or len(vertex.decision.encode('utf-8')) > OUTPUT_BYTES:
                raise PolicyFormatError('incomplete reduced terminal decision')
            decisions[id(vertex)] = {vertex.decision: vertex}
        else:
            outcomes = {}
            for child in children:
                for decision, expression in decisions[id(child)].items():
                    analysis_step()
                    continuation = expression if vertex.type == 'start' else combine('require-all', [vertex, expression])
                    outcomes.setdefault(decision, []).append(continuation)
            decisions[id(vertex)] = {decision: combine('require-any', expressions) for decision, expressions in outcomes.items()}
        slots += len(decisions[id(vertex)])
        if slots > MAX_ITEMS: raise PolicyFormatError('reduced Boolean outcome table exceeds limit')
    outcomes = {}
    for start in starts:
        for decision, expression in decisions[id(start)].items():
            analysis_step()
            outcomes.setdefault(decision, []).append(expression)
    results = []
    for decision, expressions in outcomes.items():
        expression = combine('require-any', expressions)
        results.append(vertex_type(expression.type, expression.value, decision, expression.is_not))
    candidate = type('Candidate', (), {'vertices':results,'edges':[],'final_vertices':results})()
    validate_graph(candidate)
    graph.vertices, graph.edges, graph.final_vertices = results, [], list(results)
    graph.reduce_changes_occurred = bool(edges)
    return graph
