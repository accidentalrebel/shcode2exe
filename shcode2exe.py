#!/usr/bin/python3

#from os import uname, system, remove, path
import os
import sys
import subprocess
from argparse import ArgumentParser

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
parser.add_argument('input',
                    help='The input file containing the shellcode.')
args = parser.parse_args()
dest = args.output

if args.output:
    filename = os.path.basename(args.output)
    filename = filename.split('.')[0]
else:
    filename = 'output'

file_input = args.input
    
if file_input and not os.path.exists(file_input):
    print('ERROR: File ' + file_input + ' does not exist!')
    sys.exit()

if args.string:
    with open(file_input, 'r', encoding='unicode_escape') as input_file:
        s = input_file.read().replace('\n', '')
        with open(filename + '.bin', 'wb') as gen_file:
            gen_file.write(b'' + bytes(s, encoding='raw_unicode_escape'))
            file_input = filename + '.bin'

asm_file_contents = '\tglobal _start\n' \
    '\tsection .text\n' \
    '_start:\n' \
    '\tincbin "' + file_input + '"\n'

with open(filename + '.asm', 'w+') as f:
    f.write(asm_file_contents)

cmd = os.getcwd() + '/tools/nasm/nasm'
if os.name != 'posix':
    cmd += '.exe'
    cmd = cmd.replace('/', '\\')
    
cmd += ' -f win' + args.architecture + ' -o ' + filename + '.obj ' + filename + '.asm' 
subprocess.check_output(cmd, shell=True)

cmd = os.getcwd() + '/tools/linkers/ld' + args.architecture
if os.name != 'posix':
    cmd += '.exe'
    cmd = cmd.replace('/', '\\')
cmd += ' -o '

if args.output:
    cmd += args.output
else:
    cmd += filename + '.exe'
    
cmd += ' ' + filename + '.obj'
subprocess.check_output(cmd, shell=True)

os.remove(filename + '.obj')
os.remove(filename + '.asm')

if os.path.exists(filename + '.bin'):
    os.remove(filename + '.bin')
