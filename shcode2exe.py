#!/usr/bin/env python3

import os
import shutil
import subprocess
from argparse import ArgumentParser

def CheckRequirementsMet(arg_vars):
    requirements = ['ld','nasm']

    for prog in requirements:
        if shutil.which(prog) is None:
            if prog == 'ld':
                print("{} is not installed or found. Ensure it is installed (e.g. 'sudo apt install binutils') and in your PATH and try again.".format(prog))
            elif prog == 'nasm':
                print("{} is not installed or found. Ensure it is installed (e.g 'sudo apt install nasm') and in your PATH and try again.".format(prog))
            else:
                print("Unmatched or unidentified requirements")
            raise SystemExit(1)
    CompileShellCode(arg_vars)

def ConvertToBin(file_input, filename):
    with open(file_input, 'r', encoding='unicode_escape') as input_file:
        s = input_file.read().replace('\n', '')
        with open(filename + '.bin', 'wb') as gen_file:
            gen_file.write(b'' + bytes(s, encoding='raw_unicode_escape'))
            file_input = filename + '.bin'
    input_file.close()
    gen_file.close()
    return file_input

def CompileShellCode(arguments):
    if arguments['output']:
        filename = os.path.basename(arguments['output']).split('.')[0]
    else:
        filename = 'output'

    file_input = arguments['input']

    if file_input and not os.path.exists(file_input):
        print('ERROR: File {} does not exist!'.format(file_input))
        raise SystemExit(1)

    if arguments['string']:
        file_input = ConvertToBin(file_input, filename)
        if arguments['verbose']:
            print("Converting input file to {}.bin".format(filename))

    asm_file_contents = '\tglobal _start\n' \
        '\tsection .text\n' \
        '_start:\n' \
        '\tincbin "' + file_input + '"\n'

    if arguments['verbose']:
        print("Writing assembly instruction to {}.asm".format(filename))
    with open(filename + '.asm', 'w+') as f:
        f.write(asm_file_contents)

    nasm_bin = 'nasm -f win' + arguments['architecture'] + ' -o ' + filename + '.obj ' + filename + '.asm'
    if arguments['verbose']:
        print("Executing: {}".format(nasm_bin))
    subprocess.check_output(nasm_bin, shell=True)

    ld_bin = 'ld'
    if arguments['architecture'] == '32':
        ld_bin = ld_bin + ' -m i386pe -o '
    elif arguments['architecture'] == '64':
        ld_bin = ld_bin + ' -m i386pep -o '

    if arguments['output']:
        ld_bin += arguments['output']
    else:
        ld_bin += filename + '.exe'

    ld_bin += ' ' + filename + '.obj'
    if arguments['verbose']:
        print("Executing: {}".format(ld_bin))
    subprocess.check_output(ld_bin, shell=True)
    if arguments['verbose']:
        print("Compiled shellcode saved as {}".format(filename))

    if not arguments['keep']:
        if arguments['verbose']:
            print("Attempting to remove {0}.obj, {0}.asm, and {0}.bin (if present)".format(filename))
        os.remove(filename + '.obj')
        os.remove(filename + '.asm')

        if os.path.exists(filename + '.bin'):
            os.remove(filename + '.bin')

def main():
    parser = ArgumentParser(description='Compile shellcode into an exe file from Windows or Linux.')
    parser.add_argument('-o',
                        '--output',
                        help='Set output exe file.')
    parser.add_argument('-s',
                        '--string',
                        action='store_true',
                        help='Set if input file contains shellcode in string format.')
    parser.add_argument('-a',
                        '--architecture',
                        choices=['32', '64'],
                        default = '32',
                        help='The windows architecture to use')
    parser.add_argument('-k',
                        '--keep',
                        action='store_true',
                        help='Keep files used in compilation')
    parser.add_argument('-V',
                        '--verbose',
                        action='store_true',
                        help='Print actions to stdout')
    parser.add_argument('input',
                        help='The input file containing the shellcode.')
    args = parser.parse_args()

    arg_vars = vars(args)

    CheckRequirementsMet(arg_vars)

if __name__ == '__main__':
    main()
