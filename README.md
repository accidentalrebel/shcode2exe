# shcode2exe (shellcode to exe)
Compile shellcode into an exe file from Windows or Linux. 

## Features
  * Can accept a shellcode blob or string (String format `\x5e\x31`)
  * Can target both 32bit or 64bit Windows architecture. 
  * Cross platform. Works on Linux or Windows.
  * No external dependencies except for Python (No need for Wine)
  * Tested working with Python v3.3 and above
  * Tested working on Windows 7 (Non SP1) and above
  
Created mainly for malware analysis but can also be used for exploit development. 

Inspired by [shellcode2exe](https://github.com/repnz/shellcode2exe).

## Usage
```
usage: shcode2exe.py [-h] [-o OUTPUT] [-s] [-a {32,64}] input

Compile a binary shellcode blob into an exe file. Can target both 32bit or 64bit architecture.

positional arguments:
  input                 The input file containing the shellcode.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Set output exe file.
  -s, --string          Set if input file contains shellcode in string format.
  -a {32,64}, --architecture {32,64}
                        The windows architecture to use
```

## Examples
Load a file with shellcode in the format of a string

```console
$ cat test.txt
\x5e\x31\xc0\xb0\x24\xcd\x80\xb0\x24\xcd\x80\xb0\x58\xbb\xad\xde\xe1\xfe\xb9\x69\x19\x12\x28\xba\x67\x45\x23\x01\xcd\x80
$ ./shcode2exe.py -s -o test-string.exe test.bin
```

Load a file with shellcode in the format of a blob

```console
$ ./shcode2exe.py -o test-blob.exe test.bin
```

Use 64 bit architecture for the output (32 bit is the default)

```console
$ ./shcode2exe.py -o test-blob.exe -a 64 test.bin
$ file test-blob.exe
test-blob.exe: PE32+ executable (console) x86-64 (stripped to external PDB), for MS Windows
```

## How it works
Program appends the shellcode binary to a barebones assembly file using the `incbin` macro. It is then automatically compiled using [NASM](https://www.nasm.us/) and then linked using [GNU Linker (ld)](https://linux.die.net/man/1/ld).

## Todos
  * Single binary release for easy deployment (So no need for Python)

## Contributing
Feel free to submit a pull request if you want to improve this tool!
