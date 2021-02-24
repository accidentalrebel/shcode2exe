ASM_FILE_NAME = 'shcode.asm'
ASM_FILE_CONTENTS = '\tglobal _start\n' \
    '\tsection .text\n' \
    '_start:\n' \
    '\tincbin "test.bin"\n'

with open(ASM_FILE_NAME, 'w+') as f:
    f.write(ASM_FILE_CONTENTS)
