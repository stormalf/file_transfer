#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os.path 
import argparse


__version__ = "1.0.8"

MAXBYTESIN=128
MAXBYTESOUT=344

def pyCryptoFileVersion():
    return f"pyCryptoFile version : {__version__}"


def get_private_key(privateKeyFile: str = ""):
    key = ''
    if privateKeyFile == "":
      homedir = os.path.expanduser("~")
      privkeyfile = homedir + '/.ssh/id_rsa'
    else:
      privkeyfile = privateKeyFile  
    with open(privkeyfile, "rb") as f :
      keytemp = f.read()
      key = RSA.importKey(keytemp)
    return key

def get_public_key(publicKeyFile: str = ""):
    key = ''
    if publicKeyFile == "":
      homedir = os. path. expanduser("~")
      pubkeyfile = homedir + '/.ssh/id_rsa.pub'
    else:
      pubkeyfile = publicKeyFile      
    with open(pubkeyfile, "rb") as f :
      keytemp = f.read()
      key = RSA.importKey(keytemp)
    return key

def encrypt_public_key(a_message, public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_msg = encryptor.encrypt(a_message)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    #encoded_encrypted_msg = base64.encodebytes(encrypted_msg)
    return encoded_encrypted_msg

def decrypt_private_key(encoded_encrypted_msg, private_key):
    encryptor = PKCS1_OAEP.new(private_key)
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    #decoded_encrypted_msg = base64.decodebytes(encoded_encrypted_msg)
    decoded_decrypted_msg = encryptor.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg


def pyCryptoFile(filename: str = "", mode: str = "encrypt", keyfile: str = "", outputfile: str = "") -> bytes :
  isFile = False
  data = b''
  isFile = os.path.exists(filename)
  if not isFile:
    print(f"File doesn't exist {filename}!")
    return data
  if mode == "encrypt":
    isFile = os.path.exists(keyfile)
    if not isFile:
      print(f"key file doesn't exist {keyfile}!")
      return data 
    if outputfile == "":
      outputfile = filename + ".enc"       
    encoded = b''
    encodedflow = b''
    output = open(outputfile, "wb")  
    public = get_public_key(keyfile)
    with open(filename, "rb") as f:
      tmp = f.read(MAXBYTESIN)
      encoded = encrypt_public_key(tmp, public)  
      encodedflow = encodedflow + encoded
      while tmp:
        tmp = f.read(MAXBYTESIN)
        encoded = encrypt_public_key(tmp, public)  
        encodedflow = encodedflow + encoded
    output.write(encodedflow)        
    output.close()
    return encodedflow
  elif mode == "decrypt":
    isFile = os.path.exists(keyfile)
    if not isFile:
      print(f"key file doesn't exist {keyfile}!")
      return data
    if outputfile == "":
      outputfile = filename + ".dec"             
    decoded = b''
    decodedflow = b''
    output = open(outputfile, "wb")  
    private = get_private_key(keyfile)
    with open(filename, "rb") as f:
      tmp =  f.read(MAXBYTESOUT)
      if len(tmp) > 0 :
        decoded = decrypt_private_key(tmp, private)
        decodedflow = decodedflow + decoded        
      while tmp:
        tmp =  f.read(MAXBYTESOUT) 
        if len(tmp) > 0:
          decoded = decrypt_private_key(tmp, private)
          decodedflow = decodedflow + decoded
    output.write(decodedflow)        
    output.close()
    return decodedflow
     

if __name__== "__main__":
    parser = argparse.ArgumentParser(description="pyCryptoFile is a python3 program that encrypts, decrypts using ssh key encryption")
    parser.add_argument('-V', '--version', help='Display the version of pyCryptoFile', action='version', version=pyCryptoFileVersion())
    parser.add_argument('-f', '--file', help='file to encrypt/decrypt', default='', required=False)
    parser.add_argument('-m', '--mode', help='encrypt/decrypt mode', default="encrypt", choices=['encrypt', 'decrypt'], required=False)
    parser.add_argument('-k', '--keyfile', help='public key file if encrypt mode or private key file if decrypt mode', default="", required=False)
    parser.add_argument('-o', '--outputfile', help='outputfile by default it will be the file with .enc or .dec extension', default="", required=False)    
    args = parser.parse_args()
    data = pyCryptoFile(filename=args.file, mode=args.mode, keyfile=args.keyfile, outputfile=args.outputfile)
    print(data)