#!/usr/bin/python3

#from os import uname, system, remove, path
import os
import sys
import subprocess
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
dest = args.output

if args.output:
    filename = os.path.basename(args.output)
    filename = filename.split('.')[0]
else:
    filename = 'output'

if args.input and not os.path.exists(args.input):
    print('ERROR: File ' + args.input + ' does not exist!')
    sys.exit()

ASM_FILE_CONTENTS = '\tglobal _start\n' \
    '\tsection .text\n' \
    '_start:\n' \
    '\tincbin "' + args.input + '"\n'

with open(filename + '.asm', 'w+') as f:
    f.write(ASM_FILE_CONTENTS)

cmd = 'tools/nasm/nasm'
if os.name != 'posix':
    cmd += '.exe'
cmd += ' -f win' + args.architecture + ' -o ' + filename + '.obj ' + filename + '.asm' 
subprocess.check_output(cmd, shell=True)

cmd = 'tools/linkers/ld' + args.architecture
if os.name != 'posix':
    cmd += '.exe'
cmd += ' -o '

if args.output:
    cmd += args.output
else:
    cmd += filename + '.exe'
    
cmd += ' ' + filename + '.obj'
subprocess.check_output(cmd, shell=True)

os.remove(filename + '.obj')
os.remove(filename + '.asm')
