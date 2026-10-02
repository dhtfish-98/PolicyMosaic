"""Run original and current CLIs, checking exact owned report differences."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from test_mosaic_safety import fixture, ALLOW, DENY, BRANCH


def terminal_forms(data):
    """Independent owned-report parser: identify action, operation and modifiers."""
    stack, forms = [], []
    for token in re.findall(r'\(|\)|[^\s()]+', data.decode('ascii')):
        if token == '(':
            form = []
            if stack: stack[-1].append(form)
            else: forms.append(form)
            stack.append(form)
        elif token == ')':
            assert stack
            stack.pop()
        else:
            assert stack
            stack[-1].append(token)
    assert not stack and forms[0] == ['version', '1']
    results = []
    for form in forms[1:]:
        action, *arguments = form
        assert action in ('allow', 'deny')
        operations = [value for value in arguments if isinstance(value, str)]
        modifiers = [value for value in arguments if isinstance(value, list)]
        assert len(operations) == 1
        assert all(modifier == ['with', 'no-report'] for modifier in modifiers)
        results.append((action, operations[0], tuple(tuple(value) for value in modifiers)))
    return results


def compare(upstream):
    observations = []
    with tempfile.TemporaryDirectory(prefix='policymosaic-report-comparison-') as temporary:
        for number, (nodes, table, labels, names) in enumerate([
            ((ALLOW, DENY), (0, 1), 'default\nfile-read*\n', ()),
            ((DENY, ALLOW), (0, 1), 'default\nfile-read*\n', ()),
            ((DENY, ALLOW, BRANCH), (0, 2), 'default\nfile-read*\n', ()),
            ((ALLOW, DENY), (0, 1), 'default\nfile-read*\n', ('ordinary-profile',)),
        ]):
            for mode in ('scheme', 'c'):
                answers = []
                for variant in ('original', 'derivative'):
                    folder = Path(temporary) / f'{number}-{mode}-{variant}'
                    folder.mkdir()
                    source, operations = folder / 'input.bin', folder / 'operations'
                    source.write_bytes(fixture(nodes, table, names))
                    operations.write_text(labels)
                    if variant == 'original':
                        command = [sys.executable, str(upstream / 'reverse-sandbox/reverse_sandbox.py')]
                        cwd = upstream / 'reverse-sandbox'
                    else:
                        command = [sys.executable, '-m', 'policymosaic.profile_decoder']
                        cwd = folder
                    command += ['-r', '17', '-o', str(operations), '-d', str(folder), str(source)]
                    if mode == 'c': command += ['--c_output']
                    result = subprocess.run(command, cwd=cwd, env=dict(os.environ,
                        PYTHONPATH=str(ROOT / 'src'), PYTHONDONTWRITEBYTECODE='1'),
                        capture_output=True, timeout=5)
                    if result.returncode:
                        raise AssertionError((variant, number, mode, result.returncode, result.stderr.decode()))
                    files = list(folder.glob('*.c' if mode == 'c' else '*.sb'))
                    assert len(files) == 1, files
                    answers.append(files[0].read_bytes())
                intentional = mode == 'scheme' and number in (0, 3)
                if intentional:
                    assert answers[0] == b'(version 1)\n(allow default)\n(deny (with no-report) file-read*)\n'
                    assert answers[1] == b'(version 1)\n(allow default)\n(deny file-read* (with no-report))\n'
                    # No reducer/condition AST is used to interpret these terminal forms.
                    semantic = terminal_forms(answers[0])
                    assert semantic == terminal_forms(answers[1])
                    assert semantic == [('allow', 'default', ()), ('deny', 'file-read*', (('with', 'no-report'),))]
                    assert nodes[table[0]][1] & 1 == 0 and nodes[table[1]][1] & 1 == 1
                else:
                    assert answers[0] == answers[1], (number, mode, answers)
                observation = {'fixture':number, 'mode':mode,
                    'original_sha256':hashlib.sha256(answers[0]).hexdigest(),
                    'sha256':hashlib.sha256(answers[1]).hexdigest(), 'bytes':len(answers[1]),
                    'status':'EXACT_MODIFIER_ORDER_CHANGE' if intentional else 'PASS'}
                if intentional:
                    observation['semantic_evidence'] = 'independent terminal-form parser identifies same action/operation/modifiers; action matches raw table terminals'
                    observation['actual_sbpl_engine'] = 'OPEN'
                observations.append(observation)
    return observations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream-root', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    observations = compare(arguments.upstream_root.resolve())
    if arguments.output: arguments.output.write_text(json.dumps(observations, indent=2) + '\n')
    print(json.dumps({'reports':len(observations), 'equal_reports':6,
        'exact_modifier_order_changes':2, 'unexpected_changes':0}))
