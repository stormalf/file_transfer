#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
from pyCryptoFile import encrypt_public_key, get_public_key
import argparse

__version__ = "1.0.0"

#it corresponds to 128 data encrypted using public key and encoded in base64. 
# If you change the length of data sent please calculate the new received length
# be careful that you can't send too much data the max data for 2048 key length is 190.
SENDBYTES = 128 

def pySendFileVersion():
    return f"pySendFile version : {__version__}"

def send_file(filename: str = "mytext.txt", testing: bool = False, host: str = "localhost", port: int = 12312, keyfile: str = "") -> None:
    #port = 12312  # Reserve a port for your service.
    sock = socket.socket()  # Create a socket object
    #to avoid address already bind
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if host == "localhost":
        host = socket.gethostname()  # Get local machine name
    sock.bind((host, port))  # Bind to the port
    sock.listen(1)  # Now wait for client connection.
    #sock.settimeout(20)


    print("Server listening....")
    data = b''
    pubkey = get_public_key(keyfile)
    while True:
        conn, addr = sock.accept()  # Establish connection with client.
        print(f"Got connection from {addr}")
        data = conn.recv(SENDBYTES)
        print(f"Server received: {data = }")

        with open(filename, "rb") as in_file:
            data_tmp = in_file.read(SENDBYTES)
            if data_tmp != b'':
                data = encrypt_public_key(data_tmp, pubkey)
            else:
                data = data_tmp                
            while data:
                conn.send(data)
                #print(f"Sent {data!r}")
                data_tmp = in_file.read(SENDBYTES)
                if data_tmp != b'':
                    data = encrypt_public_key(data_tmp, pubkey)
                else:
                    data = data_tmp

        print("Done sending")
        conn.close()
        if testing or data_tmp == b'':  # Allow the test to complete
            break

    sock.shutdown(1)
    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pySendFile is a python3 program that creates a socket and transfers using ssh key encryption")
    parser.add_argument('-V', '--version', help='Display the version of pySendFile', action='version', version=pySendFileVersion())
    parser.add_argument('-f', '--file', help='file to send', required=True)
    parser.add_argument('-hn', '--hostname', help='hostname', default='localhost', required=False)
    parser.add_argument('-p', '--port', help='port number', type=int, default=12312, required=False)
    parser.add_argument('-k', '--keyfile', help='public key file', default="", required=False)
    args = parser.parse_args()
    send_file(filename=args.file, host=args.hostname, port=args.port, keyfile=args.keyfile)
