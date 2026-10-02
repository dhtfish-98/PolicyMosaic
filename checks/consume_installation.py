"""Independent installed consumer; invoke with python -I outside the source tree."""
from pathlib import Path
import importlib
import importlib.metadata
import io
import json
import os
import struct
import subprocess
import sys
import tempfile

package=importlib.import_module('policymosaic')
location=Path(package.__file__).resolve()
assert 'site-packages' in location.parts,location
assert importlib.metadata.version('policymosaic')=='1.0.2'
from policymosaic.regex_bytecode import mosaic_parse
from policymosaic.filter_catalog import mosaic_Filters
from policymosaic.string_bytecode import mosaic_SandboxString
from policymosaic.profile_decoder import mosaic_parse_profile
from policymosaic.safety import PolicyFormatError
records=[];mosaic_parse(b'\x02.',0,records)
assert records==[{'pos':-6,'type':'character','value':'[.]'}]
assert mosaic_Filters.filters
assert mosaic_SandboxString().parse_byte_string(b'\x40a\x0a',[])==['a']
try:mosaic_SandboxString().parse_byte_string(b'\x40a',[])
except PolicyFormatError:pass
else:raise AssertionError('incomplete installed bytecode accepted')

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
    assert (root/'profile.sb').read_text().startswith('(version 1)\n(allow default)\n(deny ')
    assert (root/'profile.bin').read_bytes()==bytes(wire)
    assert not (root/'reverse.log').exists()
    original=(root/'profile.sb').read_bytes()
    result=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==2 and (root/'profile.sb').read_bytes()==original
    (root/'bad.bin').write_bytes(b'\0')
    result=subprocess.run(command[:-1]+[str(root/'bad.bin')],cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==2 and b'Traceback' not in result.stderr
    assert not (root/'bad.sb').exists()
    # Installed native-worker module must resolve independently, without source paths.
    result=subprocess.run([sys.executable,'-I','-m','policymosaic.emulation_worker','--address','4096','--code','1f2003d5','--mode','profile'],cwd=root,env=env,capture_output=True,timeout=5)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)=={'reference':0,'size':0}
print('PolicyMosaic 1.0.2 installed consumer PASS')
