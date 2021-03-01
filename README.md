# shcode2exe (shellcode to exe)
Compile shellcode into an exe file from Windows or Linux. 

## Features
  * Can accept a shellcode blob or string (String format `\x5e\x31`)
  * Can target both 32bit or 64bit Windows architecture. 
  * Cross platform. Works on Linux or Windows.
  * No dependency on Wine when running on Linux
  * Tested working with Python v3.3 and above
  * Tested working on Windows 7 (Non SP1) and above
  
Created mainly for malware analysis but can also be used for exploit development. 

Inspired by [shellcode2exe](https://github.com/repnz/shellcode2exe).

## Dependencies
  * [Netwide Assembler (NASM)](https://www.nasm.us/)
  * [GNU Linker](https://linux.die.net/man/1/ld)
  
For Linux, install the above dependencies via a package manager. 

```
$ sudo apt install nasm
$ sudo apt install binutils
```

For Windows, you can install nasm from [here](https://www.nasm.us/). As for the linker, you can get the 64-bit version of `ld.exe` by installing [MingW-w64](http://mingw-w64.org/doku.php). 

As an alternative, the binaries for both the compiler and linkers are also included in the tools folders. Add them to your paths to use them. It is however advisable for users to install the latest versions directly using the steps above.

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
\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x8b\xec\x55\x8b\xec\x68\x65\x78\x65\x20\x68\x63\x6d\x64\x2e\x8d\x45\xf8\x50\xb8\x44\x80\xbf\x77\xff\xd0
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

## Shellcode Samples
I've included two samples in this repository. 

  * test.bin - Is a file containing a shellcode blob
  * test.txt - Is a file containing a shellcode string

You can also generate shellcode samples using the Metasploit tool [msfvenom](https://github.com/rapid7/metasploit-framework/wiki/How-to-use-msfvenom).

Here's an example on how to generate a simple Windows exec payload:

```console
$ msfvenom -a x86 --platform windows -p windows/exec cmd=calc.exe -o test2.bin
```

## How it works
Program appends the shellcode binary to a barebones assembly file using the `incbin` macro. It is then automatically compiled using [NASM](https://www.nasm.us/) and then linked using [GNU Linker (ld)](https://linux.die.net/man/1/ld).

## Todos
  * Single binary release for easy deployment (So no need for Python)

## Contributing
Feel free to submit a pull request if you want to improve this tool!
