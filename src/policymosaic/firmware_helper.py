#!/usr/bin/env python3
# Derived from sandblaster_26 helpers/extract_sb.py; upstream BSD-3 attribution retained.
"""Optional authorized firmware inspection, with explicit process/emulation limits."""
import os
import json
import re
import stat
import tempfile
import sys
import subprocess as mosaic_subprocess
from argparse import ArgumentParser as mosaic_ArgumentParser
from pathlib import Path as mosaic_Path
import unicorn.arm64_const
import unicorn as mosaic_unicorn
import policymosaic_boundary as _name_boundary
from policymosaic.safety import PolicyFormatError, run_tool, read_local, safe_component, write_exclusive, INPUT_BYTES, OUTPUT_BYTES, MAX_NODES


def _regular(path, maximum=2 * 1024 * 1024 * 1024):
    path = mosaic_Path(path).absolute()
    descriptor = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, 'O_NOFOLLOW', 0))
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= maximum:
            raise PolicyFormatError('firmware input must be a bounded regular file')
    finally:
        os.close(descriptor)
    return path


def _owned_output(output, directory):
    path = mosaic_ipsw_get_out_path(output)
    if not path.is_absolute():
        path = directory / path
    path = path.absolute()
    try:
        path.relative_to(directory.absolute())
    except ValueError as error:
        raise PolicyFormatError('helper output lies outside its workspace') from error
    # resolve catches intermediate symbolic-link escapes; _regular rejects final links.
    try:
        path.resolve().relative_to(directory.resolve())
    except ValueError as error:
        raise PolicyFormatError('helper output escaped through a symbolic link') from error
    return _regular(path)


def mosaic_ipsw_get_out_path(output):
    if not isinstance(output, str) or len(output.encode('utf-8')) > OUTPUT_BYTES:
        raise PolicyFormatError('invalid helper path output')
    candidates = []
    for line in output.splitlines():
        if line.startswith('Created ') or line.startswith('kernelcache already exists '):
            value = line.rsplit(' ', 1)[-1]
            if not value or '\0' in value or any(ord(character) < 32 for character in value):
                raise PolicyFormatError('invalid helper output path')
            candidates.append(mosaic_Path(value))
    if not candidates:
        raise PolicyFormatError('helper did not report an output path')
    return candidates[-1]


def mosaic_dl_kernel(device, version, *, directory=None):
    if not isinstance(device, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9,._-]{0,63}', device):
        raise PolicyFormatError('invalid device selector')
    if not isinstance(version, str) or not re.fullmatch(r'[0-9][A-Za-z0-9 ._-]{0,63}', version):
        raise PolicyFormatError('invalid firmware version selector')
    workspace = mosaic_Path(directory or tempfile.mkdtemp(prefix='policymosaic-firmware-')).absolute()
    output = run_tool(['ipsw', '--no-color', 'download', 'appledb', '--os', 'iOS',
        '--version', version, '--device', device, '--kernel', '-y'], text=True,
        timeout=300, cwd=workspace)
    return _owned_output(output, workspace)


def mosaic_disassemble(path):
    path = _regular(path)
    return run_tool(['ipsw', '--no-color', 'macho', 'disass', path, '-x', '__TEXT_EXEC.__text'],
                    text=True, maximum=OUTPUT_BYTES, timeout=60).splitlines()


def _instruction(line):
    if not isinstance(line, str) or len(line) > 4096:
        raise PolicyFormatError('invalid disassembly line')
    match = re.fullmatch(r'\s*([0-9A-Fa-f]+):?\s{2,}((?:[0-9A-Fa-f]{2} ?){4})\s{2,}(.+)', line)
    if not match:
        raise PolicyFormatError('unsupported disassembly line')
    address = int(match.group(1), 16)
    code = bytes.fromhex(match.group(2))
    if address >= 2 ** 64 or address % 4 or len(code) != 4:
        raise PolicyFormatError('invalid ARM64 instruction address or width')
    return address, code, match.group(3)


def mosaic_get_bytes(lines):
    if not isinstance(lines, (list, tuple)) or not 0 < len(lines) <= MAX_NODES:
        raise PolicyFormatError('disassembly instruction count exceeds limit or is empty')
    output = bytearray()
    base = None
    for line in lines:
        address, code, _ = _instruction(line)
        if base is None:
            base = address
        if address != base + len(output) or address + len(code) >= 2 ** 64:
            raise PolicyFormatError('non-contiguous disassembly instructions')
        output.extend(code)
    return base, bytes(output)


@_name_boundary.class_contract('Emulator', {'hook_unmapped': 'mosaic_hook_unmapped', 'addr': 'mosaic_addr', 'code': 'mosaic_code', 'emu': 'mosaic_emu'})
class mosaic_Emulator:
    def __init__(self, addr, code):
        if type(addr) is not int or addr < 0 or addr % 4 or not isinstance(code, bytes) or not code or len(code) % 4 or len(code) > MAX_NODES * 4 or addr + len(code) >= 2 ** 64:
            raise PolicyFormatError('invalid emulator code span')
        self.addr = addr
        self.code = code
        self.emu = mosaic_unicorn.Uc(mosaic_unicorn.UC_ARCH_ARM64, mosaic_unicorn.UC_MODE_ARM)
        self._base = addr & ~16383
        size = ((addr + len(code) - self._base + 16383) // 16384) * 16384
        self.emu.mem_map(self._base, size)
        self.emu.mem_write(addr, code)
        self._mapped_bytes = size
        self._completed = False
        self.emu.hook_add(mosaic_unicorn.UC_HOOK_CODE, self._instruction_hook)

    def _instruction_hook(self, emu, address, size, data):
        if not self.addr <= address < self.addr + len(self.code) or size != 4:
            raise PolicyFormatError('emulation left the selected instruction span')

    def mosaic_hook_unmapped(self, write_hook=None, read_hook=None):
        def bounded_hook(callback):
            def hook(emu, access, address, size, value, data):
                if self._mapped_bytes + 16384 > 1024 * 1024:
                    raise PolicyFormatError('emulator mapping limit reached')
                self._mapped_bytes += 16384
                return callback(emu, access, address, size, value, data)
            return hook
        if write_hook:
            self.emu.hook_add(mosaic_unicorn.UC_HOOK_MEM_WRITE_UNMAPPED, bounded_hook(write_hook))
        if read_hook:
            self.emu.hook_add(mosaic_unicorn.UC_HOOK_MEM_READ_UNMAPPED, bounded_hook(read_hook))

    def __enter__(self):
        try:
            self.emu.emu_start(self.addr, self.addr + len(self.code), timeout=2_000_000, count=65536)
            if self.emu.reg_read(mosaic_unicorn.arm64_const.UC_ARM64_REG_PC) != self.addr + len(self.code):
                raise PolicyFormatError('emulation stopped before completing the selected instructions')
            self._completed = True
            return self
        except mosaic_unicorn.UcError as error:
            raise PolicyFormatError('selected instructions could not be emulated') from error
        finally:
            self.emu.emu_stop()

    def __exit__(self, *args):
        self.emu.emu_stop()


def mosaic_macho_read_data(macho, addr, size):
    if type(addr) is not int or not 0 <= addr < 2 ** 64 or type(size) is not int or not 0 < size <= INPUT_BYTES or addr + size >= 2 ** 64:
        raise PolicyFormatError('invalid or over-limit firmware profile span')
    result = run_tool(['ipsw', '--no-color', 'macho', 'dump', _regular(macho), f'{addr:#x}',
                       '--size', str(size), '--bytes'], maximum=INPUT_BYTES)
    if len(result) != size:
        raise PolicyFormatError('firmware helper returned a truncated profile')
    return result


def _emulate(address, code, mode):
    if type(address) is not int or not 0 <= address < 2 ** 64 or not isinstance(code, bytes) or not 0 < len(code) <= MAX_NODES * 4 or mode not in ('profile', 'platform'):
        raise PolicyFormatError('invalid emulation request')
    result = run_tool([sys.executable, '-m', 'policymosaic.emulation_worker',
                      '--address', str(address), '--code', code.hex(), '--mode', mode],
                      timeout=10, maximum=4096, text=True)
    try:
        values = json.loads(result)
    except ValueError as error:
        raise PolicyFormatError('native emulation returned an invalid result') from error
    if not isinstance(values, dict) or set(values) != {'reference', 'size'} or any(type(values[key]) is not int or not 0 <= values[key] < 2 ** 64 for key in values):
        raise PolicyFormatError('native emulation returned an invalid pointer result')
    return values['reference'], values['size']

@_name_boundary.class_contract('Sandbox', {'get_sb_kext': 'mosaic_get_sb_kext', '_get_nop': 'mosaic__get_nop', '_get_lines': 'mosaic__get_lines', '_get_load_platform_lines': 'mosaic__get_load_platform_lines', 'get_platform_profile_bytes': 'mosaic_get_platform_profile_bytes', 'get_profile_bytes': 'mosaic_get_profile_bytes', 'get_operations': 'mosaic_get_operations', 'decompile_sb': 'mosaic_decompile_sb', 'decompile_all': 'mosaic_decompile_all', 'kc': 'mosaic_kc', 'macho': 'mosaic_macho', 'platform_base_addr': 'mosaic_platform_base_addr', 'version': 'mosaic_version', 'dis': 'mosaic_dis', 'ops_file': 'mosaic_ops_file'})
class mosaic_Sandbox:
    def __init__(self, kc, version, *, workspace=None):
        self.kc = _regular(kc)
        if type(version) is not int or not 17 <= version <= 26:
            raise PolicyFormatError('unsupported firmware layout selector')
        self.version = version
        self._workspace = mosaic_Path(workspace or tempfile.mkdtemp(prefix='policymosaic-extraction-')).absolute()
        self.macho = self.get_sb_kext()
        self.platform_base_addr = None
        self.dis = mosaic_disassemble(self.macho)
        self.ops_file = None

    def mosaic_get_sb_kext(self):
        output = run_tool(['ipsw', '--no-color', 'kernel', 'extract', self.kc,
            'com.apple.security.sandbox'], text=True, timeout=60, cwd=self._workspace)
        return _owned_output(output, self._workspace)

    def mosaic__get_nop(self, line):
        address, _, instruction = _instruction(line)
        return f'{address:x}:  1f 20 03 d5   nop ; {instruction.replace(" ", "_")}'

    def mosaic__get_lines(self, name):
        safe_component(name)
        found = False
        lines = []
        for line in self.dis:
            if not found and any(mark in line for mark in ('; loc_', ' b\t', 'cbz\t')):
                lines.clear()
                continue
            if f'"{name}"' in line:
                found = True
            elif any(mark in line for mark in ('pacia\t', 'pacibsp', 'b.ne\t', 'ldaddal\t')):
                line = self._get_nop(line)
            elif ' bl\t' in line:
                if found:
                    break
                line = self._get_nop(line)
            lines.append(line)
            if len(lines) > MAX_NODES:
                raise PolicyFormatError('profile extraction instruction limit reached')
        if not found or not lines:
            raise PolicyFormatError('profile extraction instructions were not found')
        return lines

    def mosaic__get_load_platform_lines(self):
        found_name = False
        found_call = False
        lines = []
        finished = False
        for line in self.dis:
            if found_call:
                lines.append(line)
                if 'stp' in line:
                    finished = True
                    break
                if len(lines) > MAX_NODES:
                    raise PolicyFormatError('platform extraction instruction limit reached')
            elif found_name and ' bl\t' in line:
                found_call = True
            elif '"builtin collection"' in line:
                found_name = True
        if not lines or not finished:
            raise PolicyFormatError('platform extraction instructions were not found')
        return lines

    def _map(self, emulator, address):
        base = address & ~16383
        emulator.mem_map(base, 16384)
        return True

    def mosaic_get_platform_profile_bytes(self):
        address, code = mosaic_get_bytes(self._get_load_platform_lines())
        reference, size = _emulate(address, code, 'platform')
        return mosaic_macho_read_data(self.macho, reference, size)

    def mosaic_get_profile_bytes(self, name):
        address, code = mosaic_get_bytes(self._get_lines(name))
        reference, size = _emulate(address, code, 'profile')
        if not reference or not size:
            raise PolicyFormatError('profile pointer and size were not observed')
        return mosaic_macho_read_data(self.macho, reference, size)

    def mosaic_get_operations(self):
        output = run_tool(['strings', '-a', self.macho], text=True)
        operations = []
        found = False
        for line in output.splitlines():
            if line == 'default':
                found = True
            if found:
                if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.*-]{0,127}', line):
                    break
                operations.append(line)
                if len(operations) > 255:
                    raise PolicyFormatError('firmware operation count exceeds wire limit')
        if not operations or len(operations) != len(set(operations)):
            raise PolicyFormatError('firmware operation labels were not found or are ambiguous')
        return operations

    def mosaic_decompile_sb(self, name, sb_bin=None, skip_decompile=False):
        profile = self.get_profile_bytes(name) if sb_bin is None else sb_bin
        if not isinstance(profile, bytes) or not 0 < len(profile) <= INPUT_BYTES:
            raise PolicyFormatError('invalid extracted profile')
        filename = safe_component(name)
        out_dir = self._workspace / filename
        out_dir.mkdir(mode=0o700, exist_ok=False)
        source = out_dir / (filename + '.bin')
        write_exclusive(source, profile, maximum=INPUT_BYTES)
        if not skip_decompile:
            if self.ops_file is None:
                raise PolicyFormatError('operations catalog has not been extracted')
            run_tool(_name_boundary.decoder_invocation('--release', str(self.version),
                '--operations_file', str(self.ops_file), '--directory', str(out_dir), str(source)), timeout=60)
        return source

    def mosaic_decompile_all(self, skip_decompile=False):
        self.ops_file = self._workspace / 'operations.txt'
        write_exclusive(self.ops_file, '\n'.join(self.get_operations()).encode('utf-8'))
        paths = [self.decompile_sb('builtin collection', skip_decompile=skip_decompile)]
        name = 'autobox collection' if self.version >= 18 else 'protobox collection'
        paths.append(self.decompile_sb(name, skip_decompile=skip_decompile))
        paths.append(self.decompile_sb('platform collection', self.get_platform_profile_bytes(), skip_decompile=skip_decompile))
        return paths


def mosaic_main():
    parser = mosaic_ArgumentParser(description='Inspect authorized firmware with ipsw and bounded Unicorn emulation; reports do not prove device behavior.')
    parser.add_argument('--device', '-d', default='iPhone16,1')
    parser.add_argument('--version', '-v', default='17.6.1')
    parser.add_argument('--kernel', help='use an existing authorized local kernel instead of downloading')
    parser.add_argument('--directory', help='parent for a fresh private helper workspace')
    parser.add_argument('--skip-decompile', '-s', action='store_true')
    args = parser.parse_args()
    try:
        workspace = mosaic_Path(tempfile.mkdtemp(prefix='policymosaic-firmware-', dir=args.directory)).absolute()
        kernel = _regular(args.kernel) if args.kernel else mosaic_dl_kernel(args.device, args.version, directory=workspace)
        release = int(args.version.split('.')[0])
        sandbox = mosaic_Sandbox(kernel, release, workspace=workspace)
        sandbox.decompile_all(skip_decompile=args.skip_decompile)
        print('Reports: ' + str(workspace))
        return 0
    except (PolicyFormatError, OSError, ValueError) as error:
        import sys
        print('PolicyMosaic: firmware inspection could not complete', file=sys.stderr)
        return 2

_name_boundary.module_contract(globals(), {'ArgumentParser': 'mosaic_ArgumentParser', 'Sandbox': 'mosaic_Sandbox', 'subprocess': 'mosaic_subprocess', 'unicorn': 'mosaic_unicorn', 'main': 'mosaic_main', 'ipsw_get_out_path': 'mosaic_ipsw_get_out_path', 'Emulator': 'mosaic_Emulator', 'disassemble': 'mosaic_disassemble', 'Path': 'mosaic_Path', 'dl_kernel': 'mosaic_dl_kernel', 'get_bytes': 'mosaic_get_bytes', 'macho_read_data': 'mosaic_macho_read_data'})
if __name__ == '__main__':
    raise SystemExit(mosaic_main())
