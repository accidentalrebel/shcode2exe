from os import uname, system

current_bit = '32'
filename = 'output'

ASM_FILE_NAME = 'shcode.asm'
ASM_FILE_CONTENTS = '\tglobal _start\n' \
    '\tsection .text\n' \
    '_start:\n' \
    '\tincbin "test.bin"\n'

with open(ASM_FILE_NAME, 'w+') as f:
    f.write(ASM_FILE_CONTENTS)

cmd = 'tools/nasm/nasm'
if uname().sysname != "Linux":
    cmd += '.exe'
cmd += ' -f win' + current_bit + ' -o shcode.obj shcode.asm' 
system(cmd)

cmd = 'tools/linkers/ld' + current_bit
if uname().sysname != "Linux":
    cmd += '.exe'
cmd += ' -o ' + filename + '.exe shcode.obj'
system(cmd)

