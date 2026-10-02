"""Isolated helper calling native Unicorn to emulate input ARM64 instructions."""
import argparse
import json
import sys
from policymosaic.firmware_helper import mosaic_Emulator, mosaic_unicorn
from policymosaic.safety import PolicyFormatError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=int, required=True)
    parser.add_argument('--code', required=True)
    parser.add_argument('--mode', choices=('profile', 'platform'), required=True)
    options = parser.parse_args()
    try:
        if len(options.code) > 32768:
            raise PolicyFormatError('emulation request exceeds limit')
        code = bytes.fromhex(options.code)
        emulator = mosaic_Emulator(options.address, code)
        stores = []

        def unmapped(emu, access, address, *arguments):
            if options.mode == 'platform':
                stores.append(address)
            emu.mem_map(address & ~16383, 16384)
            return True

        emulator.hook_unmapped(write_hook=unmapped,
                              read_hook=unmapped if options.mode == 'profile' else None)
        with emulator:
            if options.mode == 'profile':
                reference = emulator.emu.reg_read(mosaic_unicorn.arm64_const.UC_ARM64_REG_X2)
                size = emulator.emu.reg_read(mosaic_unicorn.arm64_const.UC_ARM64_REG_X3)
            else:
                if not stores:
                    raise PolicyFormatError('platform pointer was not observed')
                value = bytes(emulator.emu.mem_read(stores[-1], 16))
                reference = int.from_bytes(value[:8], 'little')
                size = int.from_bytes(value[8:], 'little')
        print(json.dumps({'reference': reference, 'size': size}, separators=(',', ':')))
        return 0
    except (PolicyFormatError, ValueError, mosaic_unicorn.UcError):
        print('PolicyMosaic: native emulation could not complete', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
