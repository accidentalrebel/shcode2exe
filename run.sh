#!/bin/sh
sudo apt-get install mingw-w64
nasm -f win32 sh.asm
i686-w64-mingw32-ld sh.obj
file a.exe

# https://github.com/hatRiot/shellme
