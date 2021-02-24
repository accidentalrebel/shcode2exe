from os import uname, system, remove, path
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output',
                    help='Set output file name.')
args = parser.parse_args()
print(args.output)

current_bit = '32'

if args.output:
    filename = path.basename(args.output)
    filename = filename.split('.')[0]
else:
    filename = 'output'

ASM_FILE_CONTENTS = '\tglobal _start\n' \
    '\tsection .text\n' \
    '_start:\n' \
    '\tincbin "test.bin"\n'

with open(filename + '.asm', 'w+') as f:
    f.write(ASM_FILE_CONTENTS)

cmd = 'tools/nasm/nasm'
if uname().sysname != "Linux":
    cmd += '.exe'
cmd += ' -f win' + current_bit + ' -o ' + filename + '.obj ' + filename + '.asm' 
system(cmd)

cmd = 'tools/linkers/ld' + current_bit
if uname().sysname != "Linux":
    cmd += '.exe'
cmd += ' -o ' + args.output + ' ' + filename + '.obj'
system(cmd)

remove(filename + '.obj')
remove(filename + '.asm')
