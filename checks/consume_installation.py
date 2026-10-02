"""Independent installed consumer; invoke with python -I outside the source tree."""
from pathlib import Path
import importlib
import importlib.metadata
import io
import json
import os
import re
import struct
import subprocess
import sys
import tempfile

package=importlib.import_module('policymosaic')
location=Path(package.__file__).resolve()
assert 'site-packages' in location.parts,location
assert importlib.metadata.version('policymosaic')=='1.0.6'
from policymosaic.regex_bytecode import mosaic_parse
from policymosaic.filter_catalog import mosaic_Filters
from policymosaic.string_bytecode import mosaic_SandboxString
from policymosaic.profile_decoder import mosaic_parse_profile
from policymosaic.safety import PolicyFormatError
from policymosaic.regex_graph import mosaic_parse_regex
records=[];mosaic_parse(b'\x02.',0,records)
assert records==[{'pos':-6,'type':'character','value':'[.]'}]
assert mosaic_Filters.filters
assert mosaic_SandboxString().parse_byte_string(b'\x40a\x0a',[])==['a']
try:mosaic_SandboxString().parse_byte_string(b'\x40a',[])
except PolicyFormatError:pass
else:raise AssertionError('incomplete installed bytecode accepted')
expressions=mosaic_parse_regex(b'\0'*6+b'\x2f\x08\0\x02a\x0a\0\0\x25\0')
assert any(re.fullmatch(expression,'') is not None for expression in expressions)
assert any(re.fullmatch(expression,'aaa') is not None for expression in expressions)
assert all(re.fullmatch(expression,'b') is None for expression in expressions)
expressions=mosaic_parse_regex(b'\0'*6+b'\x02+\x25\0')
assert len(expressions)==1 and re.fullmatch(expressions[0],'+')
from policymosaic.rule_graph import ReducedGraph, ReducedVertice
graph=ReducedGraph()
vertices=[ReducedVertice(value=value,decision='allow (with report)') for value in (1,2,3)]
for vertex in vertices:graph.add_vertice(vertex)
graph.add_edge_by_vertices(vertices[0],vertices[1]);graph.add_edge_by_vertices(vertices[1],vertices[2])
graph.reduce_graph()
assert len(graph.vertices)==1 and graph.edges==[] and graph.final_vertices==graph.vertices
assert graph.vertices[0].type=='require-all' and [vertex.value for vertex in graph.vertices[0].value]==[1,2,3]
assert graph.vertices[0].decision=='allow (with report)' and [vertex.value for vertex in vertices]==[1,2,3]

with tempfile.TemporaryDirectory(prefix='policymosaic-consumer-') as folder:
    root=Path(folder)
    wire=bytearray(struct.pack('<HHBBBxHHHH',0,2,2,0,0,0,0,0,0))
    wire.extend(struct.pack('<H',1));wire.extend(b'\0'*(24-len(wire)))
    wire.extend(bytes((1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0)))
    (root/'profile.bin').write_bytes(wire)
    (root/'operations').write_text('default\nfile-read*\n')
    env={key:value for key,value in os.environ.items() if key!='PYTHONPATH'}
    command=[sys.executable,'-I','-m','policymosaic.profile_decoder','-r','17','-o',str(root/'operations'),'-d',str(root),str(root/'profile.bin')]
    result=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==0,result.stderr
    assert (root/'profile.sb').read_text() == '(version 1)\n(allow default)\n(deny file-read* (with no-report))\n'
    assert (root/'profile.bin').read_bytes()==bytes(wire)
    assert not (root/'reverse.log').exists()
    original=(root/'profile.sb').read_bytes()
    result=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==2 and (root/'profile.sb').read_bytes()==original
    (root/'bad.bin').write_bytes(b'\0')
    result=subprocess.run(command[:-1]+[str(root/'bad.bin')],cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==2 and b'Traceback' not in result.stderr
    assert not (root/'bad.sb').exists()
    # An installed ordinary branch must preserve its raw matched/unmatched action.
    header=struct.pack('<HHBBBxHHHH',0,3,2,0,0,0,0,0,0)
    layout=mosaic_parse_profile(io.BytesIO(header),type('Args',(),{'release':'17'})())
    branch_wire=bytearray(layout.base_addr)
    branch_wire[:16]=header
    branch_wire[layout.profiles_offset:layout.profiles_offset+4]=struct.pack('<HH',0,2)
    branch_wire[layout.operation_nodes_offset:layout.base_addr]=bytes((1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0))+struct.pack('<BBHHH',0,13,6,1,0)
    (root/'branch.bin').write_bytes(branch_wire)
    result=subprocess.run(command[:-1]+[str(root/'branch.bin')],cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==0,result.stderr
    assert (root/'branch.sb').read_text()=='(version 1)\n(allow default)\n(deny file-read* (with no-report)\n\t(socket-protocol 6))\n'
    assert (root/'branch.bin').read_bytes()==bytes(branch_wire)
    # Installed native-worker module must resolve independently, without source paths.
    result=subprocess.run([sys.executable,'-I','-m','policymosaic.emulation_worker','--address','4096','--code','1f2003d5','--mode','profile'],cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)=={'reference':0,'size':0}
print('PolicyMosaic 1.0.6 installed consumer PASS')
