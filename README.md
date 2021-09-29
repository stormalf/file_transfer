# file_transfer

Inspired from https://github.com/TheAlgorithms/Python/file_transfer

python socket file transfer using ssh key for encryption/decryption

This project contains 3 python modules that can be called separately.

## pyCryptoFile

This module can be called in command line :
python3 pyCryptoFile.py -h

    usage: pyCryptoFile.py [-h] [-V] [-f FILE] [-m {encrypt,decrypt}] [-k KEYFILE]

    pyCryptoFile is a python3 program that encrypts, decrypts using ssh key encryption

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pyCryptoFile
    -f FILE, --file FILE  file to encrypt/decrypt
    -m {encrypt,decrypt}, --mode {encrypt,decrypt}
                            encrypt/decrypt mode
    -k KEYFILE, --keyfile KEYFILE
                            public key file if encrypt mode or private key file if decrypt mode

example to encrypt a file content and put in another file :
python3 pyCryptoFile.py -f mytext2.txt -k ~/.ssh/id_rsa.pub > mytextcrypted.txt

example to decrypt a file content and put in another file :
python3 pyCryptoFile.py -f mytextcrypted.txt -k ~/.ssh/id_rsa -m decrypt > mydecrypted.txt

This module provides some useful functions

## pySendFile

This module can be called in command line and starts the server in the listening port default 12312 :
python3 pySendFile.py -h

    usage: pySendFile.py [-h] [-V] -f FILE [-hn HOSTNAME] [-p PORT] [-k KEYFILE]

    pySendFile is a python3 program that creates a socket and transfers using ssh key encryption

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pySendFile
    -f FILE, --file FILE  file to send
    -hn HOSTNAME, --hostname HOSTNAME
                            hostname
    -p PORT, --port PORT  port number
    -k KEYFILE, --keyfile KEYFILE
                            public key file

## pyReceiveFile

python3 pyReceiveFile.py -h
This module can be called in command line and connects to the host/port and receives the data :

    usage: pyReceiveFile.py [-h] [-V] [-f FILE] [-hn HOSTNAME] [-p PORT] [-k KEYFILE]

    pyReceiveFile is a python3 program that connects to a socket and receives data encrypted using ssh key encryption

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of pyReceiveFile
    -f FILE, --file FILE  file to receive data
    -hn HOSTNAME, --hostname HOSTNAME
                            hostname
    -p PORT, --port PORT  port number
    -k KEYFILE, --keyfile KEYFILE
                            private key file

## Examples

python3 pySendFile.py -f mytext.txt -hn localhost -p 12000
Server listening....
Got connection from ('127.0.0.1', 39704)
Server received: data = b'Hello server TOTO-7Z845TT'
Done sending

python3 pyReceiveFile.py -f result.txt -hn localhost -p 12000
File opened
Receiving data...
data = b'Hello\nThis is sample data\n\xc2\xabk\xc3\xbc\xc3\x9f\xc3\xae\xc2\xbb\n\xe2\x80\x9c\xd0\x8c\xcf\x8d\xd0\x91\xd0\x87\xe2\x80\x9d\n\xf0\x9f\x98\x80\xf0\x9f\x98\x89\n\xf0\x9f\x98\x8b\n'
Successfully got the file
Connection closed
