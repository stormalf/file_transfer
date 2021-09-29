#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket 
from pyCryptoFile import decrypt_private_key, get_private_key
import argparse

__version__ = "1.0.0"

#it corresponds to 128 data encrypted using public key and encoded in base64. 
# If you change the length of data sent please calculate the new received length
# be careful that you can't send too much data the max data for 2048 key length is 190.
RCVBYTES = 344

def pyReceiveFileVersion():
    return f"pyReceiveFile version : {__version__}"


def receive_file(filename: str = "Received_File", host: str = "localhost", port: int = 12312, keyfile: str = "") -> None: 
    sock = socket.socket()  # Create a socket object
    if host == "localhost":
        host = socket.gethostname()  # Get local machine name
    #port = 12312
    message = "Hello server " + host
    sock.settimeout(20)
    bMessage = bytes(message, "UTF-8")
    sock.connect((host, port))
    sock.send(bMessage)
    privkey = get_private_key(keyfile)

    with open(filename, "wb") as out_file:
        print("File opened")
        print("Receiving data...")
        while True:
            data_temp = sock.recv(344)
            #print(data_temp)
            if data_temp != b'':
                data = decrypt_private_key(data_temp, privkey)
                print(f"{data = }")
            else:
                data = data_temp
            if not data:
                break
            out_file.write(data)  # Write data to a file

    print("Successfully got the file")
    sock.shutdown(1)
    sock.close()
    print("Connection closed")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pyReceiveFile is a python3 program that connects to a socket and receives data encrypted using ssh key encryption")
    parser.add_argument('-V', '--version', help='Display the version of pyReceiveFile', action='version', version=pyReceiveFileVersion())
    parser.add_argument('-f', '--file', help='file to receive data', default='Received_file', required=False)
    parser.add_argument('-hn', '--hostname', help='hostname', default='localhost', required=False)
    parser.add_argument('-p', '--port', help='port number', type=int, default=12312, required=False)
    parser.add_argument('-k', '--keyfile', help='private key file', default="", required=False)
    args = parser.parse_args()
    receive_file(filename=args.file, host=args.hostname, port=args.port, keyfile=args.keyfile)

