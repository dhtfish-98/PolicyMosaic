"""Ordinary policy decisions compiled from a DAG without mutating branch polarity.

Entitlement bindings and inline policy references still use the attributed
compatibility reducer. This module does not infer their contextual semantics.
"""
from dataclasses import dataclass
import copy
import re
from policymosaic.safety import (PolicyFormatError, MAX_NODES, MAX_DEPTH, MAX_ITEMS,
    OUTPUT_BYTES, ReportBuffer, analysis_step, analysis_guard)


@dataclass(frozen=True)
class Condition:
    uid: int
    kind: str
    children: tuple
    key: tuple
    text: str
    size: int
    depth: int


class _Conditions:
    def __init__(self):
        self.nodes = {}
        self.predicates = {}
        self.predicate_bytes = 0
        self.false = self._make('false', ())
        self.true = self._make('true', ())

    def _make(self, kind, children, key=(), text=''):
        analysis_step()
        signature = kind, tuple(child.uid for child in children), key
        existing = self.nodes.get(signature)
        if existing is not None: return existing
        depth = 1 + max((child.depth for child in children), default=0)
        size = len(text.encode('utf-8')) + sum(child.size for child in children) + 16 + len(children)
        if len(self.nodes) >= MAX_ITEMS or depth > MAX_DEPTH or size > OUTPUT_BYTES:
            raise PolicyFormatError('decision expression count/depth/expansion exceeds limit')
        condition = Condition(len(self.nodes),kind,children,key,text,size,depth)
        self.nodes[signature] = condition
        return condition

    def predicate(self, node):
        branch = node.non_terminal
        if not isinstance(branch.filter, str) or not branch.filter:
            raise PolicyFormatError('decision predicate has not been converted')
        if not (branch.argument is None or isinstance(branch.argument, str) or
                isinstance(branch.argument, list) and all(isinstance(item, str) for item in branch.argument)):
            raise PolicyFormatError('invalid decision predicate argument')
        snapshot = copy.copy(branch)
        if isinstance(snapshot.argument, list): snapshot.argument = list(snapshot.argument)
        try:
            text = str(snapshot)
        except (TypeError, AttributeError, IndexError, KeyError) as error:
            raise PolicyFormatError('decision predicate data is incomplete') from error
        key = branch.filter_id, branch.argument_id, text
        if key not in self.predicates:
            self.predicate_bytes += len(text.encode('utf-8'))
            if self.predicate_bytes > OUTPUT_BYTES:
                raise PolicyFormatError('decision predicate data exceeds limit')
            self.predicates[key] = self._make('predicate', (), key, text)
        return self.predicates[key]

    def negate(self, condition):
        if condition is self.true: return self.false
        if condition is self.false: return self.true
        if condition.kind == 'not': return condition.children[0]
        return self._make('not', (condition,))

    def combine(self, kind, *conditions):
        identity, absorbing = (self.true, self.false) if kind == 'all' else (self.false, self.true)
        children, present = [], set()
        for condition in conditions:
            analysis_step()
            for child in condition.children if condition.kind == kind else (condition,):
                analysis_step()
                if child is absorbing: return absorbing
                if child is identity or child.uid in present: continue
                opposite = self.negate(child)
                if opposite.uid in present: return absorbing
                children.append(child);present.add(child.uid)
        if not children: return identity
        if len(children) == 1: return children[0]
        return self._make(kind, tuple(children))

    def select(self, predicate, matched, unmatched):
        if matched is unmatched: return matched
        return self.combine('any',self.combine('all',predicate,matched),self.combine('all',self.negate(predicate),unmatched))


@dataclass(frozen=True)
class Outcome:
    action: str
    modifiers: str
    raw: tuple


@dataclass(frozen=True)
class Rule:
    outcome: Outcome
    condition: Condition


@dataclass(frozen=True)
class DecisionPlan:
    default: Outcome
    rules: tuple
    predicates: tuple

    @analysis_guard
    def emit(self, operation, output):
        if not isinstance(operation, str) or re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.*-]{0,127}', operation) is None:
            raise PolicyFormatError('invalid operation label')
        report=ReportBuffer()
        for rule in self.rules:
            analysis_step()
            outcome, condition = rule.outcome, rule.condition
            if condition.kind == 'false' or outcome == self.default: continue
            report.write('(%s %s%s' % (outcome.action, operation, outcome.modifiers))
            if condition.kind != 'true':
                report.write('\n\t' + render_condition(condition))
            report.write(')\n')
        output.write(report.getvalue())


def _outcome(node):
    if not isinstance(node.raw, (tuple,list,bytes)) or len(node.raw) != 8 or any(type(byte) is not int or not 0 <= byte <= 255 for byte in node.raw):
        raise PolicyFormatError('invalid terminal decision record')
    terminal = node.terminal
    if terminal is None or terminal.type not in (0,1):
        raise PolicyFormatError('unsupported terminal policy decision')
    action = 'allow' if terminal.type == 0 else 'deny'
    try:
        text = str(terminal)
    except (TypeError, AttributeError, IndexError, KeyError) as error:
        raise PolicyFormatError('terminal modifier data is incomplete') from error
    if not (text == action or text.startswith(action + ' ')) or len(text.encode('utf-8')) > OUTPUT_BYTES:
        raise PolicyFormatError('invalid terminal decision presentation')
    return Outcome(action, text[len(action):], tuple(node.raw[1:]))


@analysis_guard
def compile_decisions(root, default):
    """Return an immutable ordinary decision plan, or None for contextual forms."""
    if default.terminal is None: raise PolicyFormatError('default operation must be terminal')
    inline=default.terminal.inline_modifier
    if inline is not None and inline.policy_op_idx: return None
    default_outcome = _outcome(default)
    visited, active, postorder, offsets, heights = set(), set(), [], {}, {}
    pending = [(root,False,1)]
    contextual = False
    while pending:
        analysis_step()
        node, leaving, depth = pending.pop()
        identity = id(node)
        if leaving:
            branch=node.non_terminal
            heights[identity]=1 if branch is None else 1+max(heights[id(branch.match)],heights[id(branch.unmatch)])
            if heights[identity] > MAX_DEPTH: raise PolicyFormatError('decision graph depth exceeds limit')
            active.remove(identity);visited.add(identity);postorder.append(node)
            continue
        if identity in active: raise PolicyFormatError('cyclic decision graph')
        if identity in visited: continue
        if type(node.offset) is not int or not 0 <= node.offset < MAX_NODES or node.offset in offsets and offsets[node.offset] is not node:
            raise PolicyFormatError('invalid or duplicate decision node index')
        offsets[node.offset] = node
        if len(offsets) > MAX_NODES or depth > MAX_DEPTH:
            raise PolicyFormatError('decision graph size/depth exceeds limit')
        if not isinstance(node.raw, (tuple,list,bytes)) or len(node.raw) != 8 or any(type(byte) is not int or not 0 <= byte <= 255 for byte in node.raw):
            raise PolicyFormatError('invalid decision node record')
        active.add(identity);pending.append((node,True,depth))
        if node.terminal is not None:
            if node.non_terminal is not None: raise PolicyFormatError('ambiguous decision node')
            inline = node.terminal.inline_modifier
            contextual |= bool(inline is not None and inline.policy_op_idx)
        else:
            branch = node.non_terminal
            if branch is None or branch.match is None or branch.unmatch is None:
                raise PolicyFormatError('missing decision graph branch')
            if branch.match_offset != branch.match.offset or branch.unmatch_offset != branch.unmatch.offset:
                raise PolicyFormatError('decision branch references do not match their records')
            contextual |= branch.filter_id in (30,31,32,160)
            pending.extend([(branch.unmatch,False,depth+1),(branch.match,False,depth+1)])
    if contextual: return None
    algebra, decisions = _Conditions(), {}
    slots = 0
    for node in postorder:
        analysis_step()
        if node.terminal is not None:
            result = {_outcome(node):algebra.true}
        else:
            branch=node.non_terminal
            matched, unmatched = decisions[id(branch.match)], decisions[id(branch.unmatch)]
            predicate = algebra.predicate(node)
            result = {}
            for outcome in dict.fromkeys((*matched,*unmatched)):
                analysis_step()
                condition = algebra.select(predicate,matched.get(outcome,algebra.false),unmatched.get(outcome,algebra.false))
                if condition is not algebra.false: result[outcome] = condition
        slots += len(result)
        if slots > MAX_ITEMS: raise PolicyFormatError('decision outcome table exceeds limit')
        decisions[id(node)] = result
    rules = tuple(Rule(outcome,condition) for outcome,condition in decisions[id(root)].items())
    return DecisionPlan(default_outcome,rules,tuple(algebra.predicates))


@analysis_guard
def render_condition(condition):
    output = ReportBuffer()
    pending = [condition]
    while pending:
        analysis_step()
        current = pending.pop()
        if isinstance(current,str): output.write(current);continue
        if current.kind == 'predicate': output.write(current.text)
        elif current.kind in ('true','false'): raise PolicyFormatError('unrepresentable constant inside decision report')
        else:
            name = {'not':'require-not','all':'require-all','any':'require-any'}[current.kind]
            output.write('('+name)
            pending.append(')')
            for child in reversed(current.children): pending.extend([child,' '])
    return output.getvalue()


@analysis_guard
def evaluate_condition(condition, assignment):
    """Evaluate abstract predicate assignments; does not query a device or policy."""
    values, pending = {}, [(condition,False)]
    while pending:
        analysis_step()
        current, leaving = pending.pop()
        if current.uid in values: continue
        if not leaving:
            pending.append((current,True));pending.extend((child,False) for child in current.children)
            continue
        if current.kind=='predicate':
            if current.key not in assignment or type(assignment[current.key]) is not bool:
                raise PolicyFormatError('missing or non-boolean predicate observation')
            value=assignment[current.key]
        elif current.kind=='true':value=True
        elif current.kind=='false':value=False
        elif current.kind=='not':value=not values[current.children[0].uid]
        elif current.kind=='all':value=all(values[child.uid] for child in current.children)
        else:value=any(values[child.uid] for child in current.children)
        values[current.uid]=value
    return values[condition.uid]
