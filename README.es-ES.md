

# shcode2exe (shellcode a exe)
Compila shellcode en un archivo exe desde Windows o Linux. 

## Características
  * Puede aceptar un blob o una cadena de shellcode (Formato de cadena `\x5e\x31`)
  * Puede dirigirse a arquitecturas de Windows de 32 o 64 bits. 
  * Multiplataforma. Funciona en Linux o Windows.
  * No depende de Wine al ejecutarse en Linux
  * Probado y funcional con Python v3.10 y superiores
  * La última versión probada y funcional en Windows 11
  
Creado principalmente para análisis de malware, pero también puede utilizarse para el desarrollo de exploits. 

Inspirado en [shellcode2exe](https://github.com/repnz/shellcode2exe).

## Dependencias
  * [Netwide Assembler (NASM)](https://www.nasm.us/)
  * [GNU Linker](https://linux.die.net/man/1/ld)
  
Para Linux, instala las dependencias anteriores a través de un administrador de paquetes. 

```
$ sudo apt install nasm
$ sudo apt install binutils
```

Para Windows, puedes instalar nasm desde [aquí](https://www.nasm.us/). En cuanto al enlazador, puedes obtener la versión de 64 bits de `ld.exe` instalando [MingW-w64](http://mingw-w64.org/doku.php). 

### Uso de las herramientas incluidas en Windows

Como alternativa, se incluyen binarios precompilados en el directorio `tools/`. Para utilizarlos:

**Command Prompt:**
```cmd
set PATH=%CD%\tools\nasm;%CD%\tools\linkers;%PATH%
python shcode2exe.py -o output.exe test.bin
```

**PowerShell:**
```powershell
$env:PATH = "$PWD\tools\nasm;$PWD\tools\linkers;$env:PATH"
python shcode2exe.py -o output.exe test.bin
```

Nota: Se recomienda instalar las últimas versiones directamente utilizando los instaladores oficiales mencionados anteriormente para entornos de producción.

## Uso
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

## Ejemplos
Cargar un archivo con shellcode en formato de cadena

```console
$ cat test.txt
\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x8b\xec\x55\x8b\xec\x68\x65\x78\x65\x20\x68\x63\x6d\x64\x2e\x8d\x45\xf8\x50\xb8\x44\x80\xbf\x77\xff\xd0
$ ./shcode2exe.py -s -o test-string.exe test.bin
```

Cargar un archivo con shellcode en formato de blob

```console
$ ./shcode2exe.py -o test-blob.exe test.bin
```

Utilizar arquitectura de 64 bits para la salida (32 bits es el valor predeterminado)

```console
$ ./shcode2exe.py -o test-blob.exe -a 64 test.bin
$ file test-blob.exe
test-blob.exe: PE32+ executable (console) x86-64 (stripped to external PDB), for MS Windows
```

## Muestras de Shellcode
He incluido dos muestras en este repositorio. 

  * test.bin - Es un archivo que contiene un blob de shellcode
  * test.txt - Es un archivo que contiene una cadena de shellcode

También puedes generar muestras de shellcode utilizando la herramienta de Metasploit [msfvenom](https://github.com/rapid7/metasploit-framework/wiki/How-to-use-msfvenom).

Aquí tienes un ejemplo de cómo generar una carga útil (payload) de exec simple para Windows:

```console
$ msfvenom -a x86 --platform windows -p windows/exec cmd=calc.exe -o test2.bin
```

## Cómo funciona
El programa agrega el binario del shellcode a un archivo de ensamblaje básico utilizando la macro `incbin`. Luego se compila automáticamente usando [NASM](https://www.nasm.us/) y se enlaza mediante [GNU Linker (ld)](https://linux.die.net/man/1/ld).

## Por hacer
  * Liberación de un solo binario para un despliegue sencillo (de modo que no sea necesario Python)

## Créditos
  * [f4yd4-s3c](https://github.com/f4yd4-s3c) - Corrección para ocultar la ventana de consola al ejecutarse en Windows

## Contribuciones
¡No dudes en enviar un pull request si deseas mejorar esta herramienta!
