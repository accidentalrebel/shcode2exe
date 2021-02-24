#!/usr/bin/python3

from os import uname, system, remove, path
import sys
from argparse import ArgumentParser

parser = ArgumentParser(description='Compile a binary shellcode blob into an exe file. Can target both 32bit or 64bit architecture.')
parser.add_argument('-o',
                    '--output',
                    help='Set output exe file.')
parser.add_argument('-a',
                    '--architecture',
                    choices=['32', '64'],
                    default = '32',
                    help='The windows architecture to use')
parser.add_argument('input',
                    help='The input file containing the shellcode.')
args = parser.parse_args()

if args.output:
    filename = path.basename(args.output)
    filename = filename.split('.')[0]
else:
    filename = 'output'

if args.input and not path.exists(args.input):
    print('ERROR: File ' + args.input + ' does not exist!')
    sys.exit()

ASM_FILE_CONTENTS = '\tglobal _start\n' \
    '\tsection .text\n' \
    '_start:\n' \
    '\tincbin "' + args.input + '"\n'

with open(filename + '.asm', 'w+') as f:
    f.write(ASM_FILE_CONTENTS)

cmd = 'tools/nasm/nasm'
if uname().sysname != "Linux":
    cmd += '.exe'
cmd += ' -f win' + args.architecture + ' -o ' + filename + '.obj ' + filename + '.asm' 
system(cmd)

cmd = 'tools/linkers/ld' + args.architecture
if uname().sysname != "Linux":
    cmd += '.exe'
cmd += ' -o ' + args.output + ' ' + filename + '.obj'
system(cmd)

remove(filename + '.obj')
remove(filename + '.asm')
