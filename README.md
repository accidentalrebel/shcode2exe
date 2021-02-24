# shcode2exe
Shellcode to exe. Compile a binary shellcode blob into an exe file from Windows or Linux. Can target both 32bit or 64bit Windows architecture. 

Inspired by [shellcode2exe](https://github.com/repnz/shellcode2exe).

## Usage
```
usage: shcode2exe.py [-h] [-o OUTPUT] [-a {32,64}] input

Compile a binary shellcode blob into an exe file. Can target both 32bit or 64bit architecture.

positional arguments:
  input                 The input file containing the shellcode.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Set output exe file.
  -a {32,64}, --architecture {32,64}
                        The windows architecture to use
```

## How it works
Program appends the shellcode binary to a barebones assembly file using the `incbin` macro. It is then automatically compiled using [NASM](https://www.nasm.us/) and then linked using [GNU Linker (ld)](https://linux.die.net/man/1/ld).

## Contributing
Feel free to submit a pull request if you want to improve this tool!
