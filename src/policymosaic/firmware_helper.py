#!/usr/bin/env python3
# Derived from helpers/extract_sb.py; original copyright and license in ORIGIN.md and LICENSE.
import policymosaic_boundary as _name_boundary
import subprocess as mosaic_subprocess
import unicorn.arm64_const as _boundary_import_unicorn_arm64_const
import unicorn as mosaic_unicorn
from argparse import ArgumentParser as mosaic_ArgumentParser
from pathlib import Path as mosaic_Path

@_name_boundary.callable_contract({'output': 'mosaic_output_8b2fd9b'}, 'ipsw_get_out_path')
def mosaic_ipsw_get_out_path(mosaic_output_8b2fd9b):
    mosaic_path_4c0673e = None
    for mosaic_l_bf8f481 in mosaic_output_8b2fd9b.split('\n'):
        if 'Created' in mosaic_l_bf8f481 or 'kernelcache already exists' in mosaic_l_bf8f481:
            mosaic_path_4c0673e = mosaic_l_bf8f481.split(' ')[-1]
    return mosaic_Path(mosaic_path_4c0673e)

@_name_boundary.callable_contract({'device': 'mosaic_device_366dab6', 'version': 'mosaic_version_8352899'}, 'dl_kernel')
def mosaic_dl_kernel(mosaic_device_366dab6, mosaic_version_8352899):
    mosaic_output_dc97693 = mosaic_subprocess.check_output(['ipsw', '--no-color', 'download', 'appledb', '--os', 'iOS', '--version', mosaic_version_8352899, '--device', mosaic_device_366dab6, '--kernel', '-y'], text=True, stderr=mosaic_subprocess.STDOUT)
    mosaic_path_4567ed8 = mosaic_ipsw_get_out_path(mosaic_output_dc97693)
    if mosaic_path_4567ed8 is None:
        raise Exception(f"Couldn't dl kernel: {mosaic_output_dc97693}")
    return mosaic_path_4567ed8

@_name_boundary.callable_contract({'path': 'mosaic_path_19c0ce2'}, 'disassemble')
def mosaic_disassemble(mosaic_path_19c0ce2):
    return mosaic_subprocess.check_output(['ipsw', '--no-color', 'macho', 'disass', mosaic_path_19c0ce2, '-x', '__TEXT_EXEC.__text'], text=True, stderr=mosaic_subprocess.STDOUT).split('\n')

@_name_boundary.callable_contract({'lines': 'mosaic_lines_08b1f85'}, 'get_bytes')
def mosaic_get_bytes(mosaic_lines_08b1f85):
    mosaic_base_3b54cb4 = 0
    mosaic_b_3d8b098 = b''
    for mosaic_l_945486e in mosaic_lines_08b1f85:
        mosaic_addr_1dd3326, mosaic_op_8997313, mosaic_dis_38739a7 = mosaic_l_945486e.split('  ')
        if mosaic_base_3b54cb4 == 0:
            mosaic_base_3b54cb4 = int(mosaic_addr_1dd3326.replace(':', ''), 16)
        mosaic_b_3d8b098 += b''.fromhex(mosaic_op_8997313)
    return (mosaic_base_3b54cb4, mosaic_b_3d8b098)

@_name_boundary.class_contract('Emulator', {'hook_unmapped': 'mosaic_hook_unmapped', 'addr': 'mosaic_addr', 'code': 'mosaic_code', 'emu': 'mosaic_emu'})
class mosaic_Emulator:

    @_name_boundary.callable_contract({'self': 'mosaic_self_93cb41e', 'addr': 'mosaic_addr_3be7667', 'code': 'mosaic_code_9c1039a'}, '__init__')
    def __init__(mosaic_self_93cb41e, mosaic_addr_3be7667, mosaic_code_9c1039a):
        _name_boundary.attributes(mosaic_self_93cb41e)['addr'] = mosaic_addr_3be7667
        _name_boundary.attributes(mosaic_self_93cb41e)['code'] = mosaic_code_9c1039a
        mosaic_base_a6056e4 = mosaic_addr_3be7667 & ~16383
        _name_boundary.attributes(mosaic_self_93cb41e)['emu'] = mosaic_unicorn.Uc(mosaic_unicorn.UC_ARCH_ARM64, mosaic_unicorn.UC_MODE_ARM)
        _name_boundary.attributes(mosaic_self_93cb41e)['emu'].mem_map(mosaic_base_a6056e4, 262144)
        _name_boundary.attributes(mosaic_self_93cb41e)['emu'].mem_write(mosaic_addr_3be7667, mosaic_code_9c1039a)

    @_name_boundary.callable_contract({'self': 'mosaic_self_2de2908', 'write_hook': 'mosaic_write_hook_b52a82d', 'read_hook': 'mosaic_read_hook_e2b25bd'}, 'hook_unmapped')
    def mosaic_hook_unmapped(mosaic_self_2de2908, mosaic_write_hook_b52a82d=None, mosaic_read_hook_e2b25bd=None):
        if mosaic_write_hook_b52a82d:
            _name_boundary.attributes(mosaic_self_2de2908)['emu'].hook_add(mosaic_unicorn.UC_HOOK_MEM_WRITE_UNMAPPED, mosaic_write_hook_b52a82d)
        if mosaic_read_hook_e2b25bd:
            _name_boundary.attributes(mosaic_self_2de2908)['emu'].hook_add(mosaic_unicorn.UC_HOOK_MEM_READ_UNMAPPED, mosaic_read_hook_e2b25bd)

    @_name_boundary.callable_contract({'self': 'mosaic_self_4319814'}, '__enter__')
    def __enter__(mosaic_self_4319814):
        _name_boundary.attributes(mosaic_self_4319814)['emu'].emu_start(_name_boundary.attributes(mosaic_self_4319814)['addr'], _name_boundary.attributes(mosaic_self_4319814)['addr'] + len(_name_boundary.attributes(mosaic_self_4319814)['code']))
        return mosaic_self_4319814

    @_name_boundary.callable_contract({'self': 'mosaic_self_0735e6b', 'args': 'mosaic_args_49ae434'}, '__exit__')
    def __exit__(mosaic_self_0735e6b, *mosaic_args_49ae434):
        _name_boundary.attributes(mosaic_self_0735e6b)['emu'].emu_stop()

@_name_boundary.callable_contract({'macho': 'mosaic_macho_62aeefe', 'addr': 'mosaic_addr_c5659bc', 'size': 'mosaic_size_1200a47'}, 'macho_read_data')
def mosaic_macho_read_data(mosaic_macho_62aeefe, mosaic_addr_c5659bc, mosaic_size_1200a47):
    return mosaic_subprocess.check_output(['ipsw', '--no-color', 'macho', 'dump', mosaic_macho_62aeefe, f'{mosaic_addr_c5659bc:#x}', '--size', f'{mosaic_size_1200a47}', '--bytes'])

@_name_boundary.class_contract('Sandbox', {'get_sb_kext': 'mosaic_get_sb_kext', '_get_nop': 'mosaic__get_nop', '_get_lines': 'mosaic__get_lines', '_get_load_platform_lines': 'mosaic__get_load_platform_lines', 'get_platform_profile_bytes': 'mosaic_get_platform_profile_bytes', 'get_profile_bytes': 'mosaic_get_profile_bytes', 'get_operations': 'mosaic_get_operations', 'decompile_sb': 'mosaic_decompile_sb', 'decompile_all': 'mosaic_decompile_all', 'kc': 'mosaic_kc', 'macho': 'mosaic_macho', 'platform_base_addr': 'mosaic_platform_base_addr', 'version': 'mosaic_version', 'dis': 'mosaic_dis', 'ops_file': 'mosaic_ops_file'})
class mosaic_Sandbox:

    @_name_boundary.callable_contract({'self': 'mosaic_self_1883a9b', 'kc': 'mosaic_kc_65756bf', 'version': 'mosaic_version_02e50bb'}, '__init__')
    def __init__(mosaic_self_1883a9b, mosaic_kc_65756bf, mosaic_version_02e50bb):
        _name_boundary.attributes(mosaic_self_1883a9b)['kc'] = mosaic_kc_65756bf
        _name_boundary.attributes(mosaic_self_1883a9b)['macho'] = _name_boundary.attributes(mosaic_self_1883a9b)['get_sb_kext']()
        _name_boundary.attributes(mosaic_self_1883a9b)['platform_base_addr'] = None
        _name_boundary.attributes(mosaic_self_1883a9b)['version'] = mosaic_version_02e50bb
        print(f"sb: {_name_boundary.attributes(mosaic_self_1883a9b)['macho']}")
        _name_boundary.attributes(mosaic_self_1883a9b)['dis'] = mosaic_disassemble(_name_boundary.attributes(mosaic_self_1883a9b)['macho'])

    @_name_boundary.callable_contract({'self': 'mosaic_self_0ce9724'}, 'get_sb_kext')
    def mosaic_get_sb_kext(mosaic_self_0ce9724):
        mosaic_output_62d18f5 = mosaic_subprocess.check_output(['ipsw', '--no-color', 'kernel', 'extract', _name_boundary.attributes(mosaic_self_0ce9724)['kc'], 'com.apple.security.sandbox'], text=True, stderr=mosaic_subprocess.STDOUT)
        mosaic_path_04501a0 = mosaic_ipsw_get_out_path(mosaic_output_62d18f5)
        if mosaic_path_04501a0 is None:
            raise Exception(f"Couldn't extract sb kext: {mosaic_output_62d18f5}")
        return mosaic_path_04501a0

    @_name_boundary.callable_contract({'self': 'mosaic_self_2f03fa9', 'line': 'mosaic_line_3f8b392'}, '_get_nop')
    def mosaic__get_nop(mosaic_self_2f03fa9, mosaic_line_3f8b392):
        mosaic_addr_8d8ca71, mosaic_op_1cbaa65, mosaic_dis_5f9c504 = mosaic_line_3f8b392.split('  ')
        return f"{mosaic_addr_8d8ca71}  1f 20 03 d5   nop ; {mosaic_dis_5f9c504.replace(' ', '_')}"

    @_name_boundary.callable_contract({'self': 'mosaic_self_289c9fd', 'name': 'mosaic_name_75a43c7'}, '_get_lines')
    def mosaic__get_lines(mosaic_self_289c9fd, mosaic_name_75a43c7):
        mosaic_found_name_c697621 = False
        mosaic_lines_558a6a6 = []
        mosaic_new_label_marks_c4f032f = ['; loc_', ' b\t', 'cbz\t']
        mosaic_skip_insts_d1ed213 = ['pacia\t', 'pacibsp', 'b.ne\t', 'ldaddal\t']
        for mosaic_l_e44ee4b in _name_boundary.attributes(mosaic_self_289c9fd)['dis']:
            mosaic_new_label_0316c7b = any([True for mosaic_m_6efeb97 in mosaic_new_label_marks_c4f032f if mosaic_m_6efeb97 in mosaic_l_e44ee4b])
            if mosaic_new_label_0316c7b and (not mosaic_found_name_c697621):
                mosaic_lines_558a6a6 = []
                continue
            if f'"{mosaic_name_75a43c7}"' in mosaic_l_e44ee4b:
                mosaic_found_name_c697621 = True
            elif any([True for mosaic_m_4257b1c in mosaic_skip_insts_d1ed213 if mosaic_m_4257b1c in mosaic_l_e44ee4b]):
                mosaic_l_e44ee4b = _name_boundary.attributes(mosaic_self_289c9fd)['_get_nop'](mosaic_l_e44ee4b)
            elif ' bl\t' in mosaic_l_e44ee4b:
                if mosaic_found_name_c697621:
                    break
                else:
                    mosaic_l_e44ee4b = _name_boundary.attributes(mosaic_self_289c9fd)['_get_nop'](mosaic_l_e44ee4b)
            mosaic_lines_558a6a6.append(mosaic_l_e44ee4b)
        if not mosaic_lines_558a6a6:
            raise Exception(f"Couldn't find code to load {mosaic_name_75a43c7} profile")
        print(f"load {mosaic_name_75a43c7} code:\n{'\n'.join(mosaic_lines_558a6a6)}")
        return mosaic_lines_558a6a6

    @_name_boundary.callable_contract({'self': 'mosaic_self_dfba451'}, '_get_load_platform_lines')
    def mosaic__get_load_platform_lines(mosaic_self_dfba451):
        mosaic_lines_60f5fd8 = []
        mosaic_found_builtin_collection_str_d972779 = False
        mosaic_found_bl_after_builtin_13e720d = False
        for mosaic_l_d54b0fa in _name_boundary.attributes(mosaic_self_dfba451)['dis']:
            if mosaic_found_bl_after_builtin_13e720d:
                mosaic_lines_60f5fd8.append(mosaic_l_d54b0fa)
                if 'stp' in mosaic_l_d54b0fa:
                    break
            if mosaic_found_builtin_collection_str_d972779:
                if ' bl\t' in mosaic_l_d54b0fa:
                    mosaic_found_bl_after_builtin_13e720d = True
                    continue
            if '"builtin collection"' in mosaic_l_d54b0fa:
                mosaic_found_builtin_collection_str_d972779 = True
                continue
        if not mosaic_lines_60f5fd8:
            raise Exception("Couldn't find code to load platform profile")
        print(f"load platform lines\n{'\n'.join(mosaic_lines_60f5fd8)}")
        return mosaic_lines_60f5fd8

    @_name_boundary.callable_contract({'self': 'mosaic_self_aa9d136'}, 'get_platform_profile_bytes')
    def mosaic_get_platform_profile_bytes(mosaic_self_aa9d136):
        mosaic_lines_a4c142b = _name_boundary.attributes(mosaic_self_aa9d136)['_get_load_platform_lines']()
        mosaic_addr_02db591, mosaic_code_4407dc9 = mosaic_get_bytes(mosaic_lines_a4c142b)

        @_name_boundary.callable_contract({'emu': 'mosaic_emu_b02b3bf', 'access': 'mosaic_access_5ee2b85', 'addr': 'mosaic_addr_777a678', 'args': 'mosaic_args_d27f6f1'}, 'hook_unmapped_write')
        def mosaic_hook_unmapped_write_661c3ef(mosaic_emu_b02b3bf, mosaic_access_5ee2b85, mosaic_addr_777a678, *mosaic_args_d27f6f1):
            _name_boundary.attributes(mosaic_self_aa9d136)['platform_base_addr'] = mosaic_addr_777a678
            mosaic_base_fd60174 = mosaic_addr_777a678 & ~16383
            mosaic_emu_b02b3bf.mem_map(mosaic_base_fd60174, 16384)
            return True
        mosaic_emu_11681bc = mosaic_Emulator(mosaic_addr_02db591, mosaic_code_4407dc9)
        _name_boundary.attributes(mosaic_emu_11681bc)['hook_unmapped'](write_hook=mosaic_hook_unmapped_write_661c3ef)
        with mosaic_emu_11681bc:
            if _name_boundary.attributes(mosaic_self_aa9d136)['platform_base_addr'] is None:
                raise Exception("load platform profile code didn't do the expected stp!")
            mosaic_platform_base_bytes_ef570e0 = _name_boundary.attributes(mosaic_emu_11681bc)['emu'].mem_read(_name_boundary.attributes(mosaic_self_aa9d136)['platform_base_addr'], 16)
        mosaic_ref_ace5348, mosaic_size_5f356b1 = (int.from_bytes(mosaic_platform_base_bytes_ef570e0[:8], byteorder='little'), int.from_bytes(mosaic_platform_base_bytes_ef570e0[8:], byteorder='little'))
        print(f'platform profile: {mosaic_ref_ace5348:#x} size: {mosaic_size_5f356b1:#x}')
        mosaic_profile_d844111 = mosaic_macho_read_data(_name_boundary.attributes(mosaic_self_aa9d136)['macho'], mosaic_ref_ace5348, mosaic_size_5f356b1)
        print(f'read platform profile {len(mosaic_profile_d844111):#x} bytes! {mosaic_profile_d844111[:32].hex()}...')
        return mosaic_profile_d844111

    @_name_boundary.callable_contract({'self': 'mosaic_self_b5f74a6', 'name': 'mosaic_name_66a156f'}, 'get_profile_bytes')
    def mosaic_get_profile_bytes(mosaic_self_b5f74a6, mosaic_name_66a156f):
        mosaic_lines_2d220f9 = _name_boundary.attributes(mosaic_self_b5f74a6)['_get_lines'](mosaic_name_66a156f)
        mosaic_addr_dc8331c, mosaic_code_1afb2c1 = mosaic_get_bytes(mosaic_lines_2d220f9)

        @_name_boundary.callable_contract({'emu': 'mosaic_emu_9b44923', 'access': 'mosaic_access_5e958b4', 'addr': 'mosaic_addr_b47c6e5', 'args': 'mosaic_args_9986235'}, 'hook_unmapped')
        def mosaic_hook_unmapped_c3a5354(mosaic_emu_9b44923, mosaic_access_5e958b4, mosaic_addr_b47c6e5, *mosaic_args_9986235):
            mosaic_base_2c3432b = mosaic_addr_b47c6e5 & ~16383
            mosaic_emu_9b44923.mem_map(mosaic_base_2c3432b, 16384)
            return True
        mosaic_emu_1f2a8bc = mosaic_Emulator(mosaic_addr_dc8331c, mosaic_code_1afb2c1)
        _name_boundary.attributes(mosaic_emu_1f2a8bc)['hook_unmapped'](mosaic_hook_unmapped_c3a5354, mosaic_hook_unmapped_c3a5354)
        with mosaic_emu_1f2a8bc:
            mosaic_ref_7056827, mosaic_size_953e2e6 = (_name_boundary.attributes(mosaic_emu_1f2a8bc)['emu'].reg_read(mosaic_unicorn.arm64_const.UC_ARM64_REG_X2), _name_boundary.attributes(mosaic_emu_1f2a8bc)['emu'].reg_read(mosaic_unicorn.arm64_const.UC_ARM64_REG_X3))
            if not mosaic_ref_7056827 or not mosaic_size_953e2e6:
                raise Exception(f"Couldn't find ref/size to {mosaic_name_66a156f} profile")
        print(f'{mosaic_name_66a156f}: {mosaic_ref_7056827:#x} size: {mosaic_size_953e2e6:#x}')
        mosaic_profile_5adedac = mosaic_macho_read_data(_name_boundary.attributes(mosaic_self_b5f74a6)['macho'], mosaic_ref_7056827, mosaic_size_953e2e6)
        print(f'read {mosaic_name_66a156f} profile {len(mosaic_profile_5adedac):#x} bytes! {mosaic_profile_5adedac[:32].hex()}...')
        return mosaic_profile_5adedac

    @_name_boundary.callable_contract({'self': 'mosaic_self_a4a54fd'}, 'get_operations')
    def mosaic_get_operations(mosaic_self_a4a54fd):
        mosaic_found_default_dc2c92f = False
        mosaic_ops_eefcd85 = []
        for mosaic_l_8ca7907 in mosaic_subprocess.check_output(['strings', _name_boundary.attributes(mosaic_self_a4a54fd)['macho']], text=True).split('\n'):
            if mosaic_l_8ca7907 == 'default':
                mosaic_found_default_dc2c92f = True
            if mosaic_found_default_dc2c92f:
                if '"' in mosaic_l_8ca7907 or ' ' in mosaic_l_8ca7907 or '%' in mosaic_l_8ca7907 or (':' in mosaic_l_8ca7907):
                    break
                mosaic_ops_eefcd85.append(mosaic_l_8ca7907)
        if not mosaic_ops_eefcd85:
            raise Exception("Couldn't find sandbox operations?")
        print(f"Found {len(mosaic_ops_eefcd85)} operations. {','.join(mosaic_ops_eefcd85[0:3])}...{mosaic_ops_eefcd85[-1]}.")
        return mosaic_ops_eefcd85

    @_name_boundary.callable_contract({'self': 'mosaic_self_51fff2a', 'name': 'mosaic_name_27d99f0', 'sb_bin': 'mosaic_sb_bin_bc68e9b', 'skip_decompile': 'mosaic_skip_decompile_a6af318'}, 'decompile_sb')
    def mosaic_decompile_sb(mosaic_self_51fff2a, mosaic_name_27d99f0, mosaic_sb_bin_bc68e9b=None, mosaic_skip_decompile_a6af318=False):
        mosaic_sb_bin_bc68e9b = mosaic_sb_bin_bc68e9b or _name_boundary.attributes(mosaic_self_51fff2a)['get_profile_bytes'](mosaic_name_27d99f0)
        mosaic_filename_31209ed = mosaic_name_27d99f0.replace(' ', '_')
        mosaic_out_dir_7ccafc3 = _name_boundary.attributes(mosaic_self_51fff2a)['macho'].parent / mosaic_filename_31209ed
        mosaic_out_dir_7ccafc3.mkdir(exist_ok=True)
        mosaic_filepath_746933f = mosaic_out_dir_7ccafc3 / (mosaic_filename_31209ed + '.bin')
        with open(mosaic_filepath_746933f, 'wb') as mosaic_f_5067d6d:
            mosaic_f_5067d6d.write(mosaic_sb_bin_bc68e9b)
        if mosaic_skip_decompile_a6af318:
            print(f'Skipping decompilation for {mosaic_name_27d99f0}')
        else:
            mosaic_args_197c9a0 = _name_boundary.decoder_invocation('--release', str(_name_boundary.attributes(mosaic_self_51fff2a)['version']), '--operations', _name_boundary.attributes(mosaic_self_51fff2a)['ops_file'].absolute(), '--directory', mosaic_out_dir_7ccafc3.absolute(), mosaic_filepath_746933f.absolute())
            print(f'running: {mosaic_args_197c9a0}')
            if mosaic_subprocess.call(mosaic_args_197c9a0, cwd=_name_boundary.resource('.')):
                print(f'ERROR: failed to decompile {mosaic_name_27d99f0} profile')

    @_name_boundary.callable_contract({'self': 'mosaic_self_5128f0c', 'skip_decompile': 'mosaic_skip_decompile_0fe88d4'}, 'decompile_all')
    def mosaic_decompile_all(mosaic_self_5128f0c, mosaic_skip_decompile_0fe88d4=False):
        _name_boundary.attributes(mosaic_self_5128f0c)['ops_file'] = _name_boundary.attributes(mosaic_self_5128f0c)['macho'].parent / 'operations.txt'
        mosaic_ops_3dbe3b2 = _name_boundary.attributes(mosaic_self_5128f0c)['get_operations']()
        with open(_name_boundary.attributes(mosaic_self_5128f0c)['ops_file'], 'w') as mosaic_f_c8657e9:
            mosaic_f_c8657e9.write('\n'.join(mosaic_ops_3dbe3b2))
        _name_boundary.attributes(mosaic_self_5128f0c)['decompile_sb']('builtin collection', skip_decompile=mosaic_skip_decompile_0fe88d4)
        mosaic_protobox_name_074b087 = 'autobox collection' if _name_boundary.attributes(mosaic_self_5128f0c)['version'] >= 18 else 'protobox collection'
        _name_boundary.attributes(mosaic_self_5128f0c)['decompile_sb'](mosaic_protobox_name_074b087, skip_decompile=mosaic_skip_decompile_0fe88d4)
        mosaic_platform_sb_2c7bf2d = _name_boundary.attributes(mosaic_self_5128f0c)['get_platform_profile_bytes']()
        _name_boundary.attributes(mosaic_self_5128f0c)['decompile_sb']('platform collection', mosaic_platform_sb_2c7bf2d, skip_decompile=mosaic_skip_decompile_0fe88d4)

@_name_boundary.callable_contract({}, 'main')
def mosaic_main():
    mosaic_parser_7d70209 = mosaic_ArgumentParser('Sandbox Extractor Helper', description='Specify device+version, and this script will do the entire process: Download the kernel cache, extract the sandbox profiles, and run the decompiler.')
    mosaic_parser_7d70209.add_argument('--device', '-d', help='Device', default='iPhone16,1')
    mosaic_parser_7d70209.add_argument('--version', '-v', help="Version, can specify a beta like '18.0 beta 4'", default='17.6.1')
    mosaic_parser_7d70209.add_argument('--skip-decompile', '-s', help='Skip sandbox decompilation (currently unsupported on iOS 18)', default=False, action='store_true')
    mosaic_args_5345ae0 = mosaic_parser_7d70209.parse_args()
    print(f"Downloading kernel cache for {mosaic_args_5345ae0.device} {_name_boundary.attributes(mosaic_args_5345ae0)['version']}.")
    mosaic_k_4efeee1 = mosaic_dl_kernel(mosaic_args_5345ae0.device, _name_boundary.attributes(mosaic_args_5345ae0)['version'])
    mosaic_release_b73f487 = int(_name_boundary.attributes(mosaic_args_5345ae0)['version'].split('.')[0])
    mosaic_sb_3430740 = mosaic_Sandbox(mosaic_k_4efeee1, mosaic_release_b73f487)
    _name_boundary.attributes(mosaic_sb_3430740)['decompile_all'](skip_decompile=mosaic_args_5345ae0.skip_decompile)
if __name__ == '__main__':
    mosaic_main()
_name_boundary.module_contract(globals(), {'ArgumentParser': 'mosaic_ArgumentParser', 'Sandbox': 'mosaic_Sandbox', 'subprocess': 'mosaic_subprocess', 'unicorn': 'mosaic_unicorn', 'main': 'mosaic_main', 'ipsw_get_out_path': 'mosaic_ipsw_get_out_path', 'Emulator': 'mosaic_Emulator', 'disassemble': 'mosaic_disassemble', 'Path': 'mosaic_Path', 'dl_kernel': 'mosaic_dl_kernel', 'get_bytes': 'mosaic_get_bytes', 'macho_read_data': 'mosaic_macho_read_data'})
