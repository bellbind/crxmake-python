#!/usr/bin/env python
# -*- mode: python coding: utf-8 -*-

"""
building google chrome extension crx with commandline
it is inspired by rubygem's crxmake
requires: M2Crypto module (and "openssl" commandline)
"""

import dircache
import hashlib
import io
import os
import struct
import subprocess
import sys
import zipfile
import M2Crypto.EVP
import M2Crypto.RSA
import M2Crypto.BIO

# read base path
if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
    print("usage: %s PACKAGE_BASE_DIR" % sys.argv[0])
    sys.exit(1)
    pass
dirname = sys.argv[1]
if dirname.endswith(os.path.sep): dirname = dirname[:-1]

# make raw zip data
zip_memory = io.BytesIO()
zf = zipfile.ZipFile(zip_memory, "w", zipfile.ZIP_DEFLATED)
def make_zip(z, path, parent):
    for ch in dircache.listdir(path):
        child = os.path.join(path, ch)
        name = "%s/%s" % (parent, ch)
        if os.path.isfile(child): z.write(child, name)
        if os.path.isdir(child): make_zip(z, child, name)
        pass
    pass
make_zip(zf, dirname, "")
zf.close()
zip_data = zip_memory.getvalue()

# load or make private key PEM
pem_name = dirname + ".pem"
private_pem = None
try:
    key = M2Crypto.RSA.load_key(pem_name)
    with open(pem_name, "r") as pem_file:
        private_pem = pem_file.read()
        pass
    pass
    print("use existing private pem: %s" % pem_name)
except:
    pass
if not private_pem:
    key = M2Crypto.RSA.gen_key(1024, 65537, lambda:None)
    private_pem = key.as_pem(cipher=None)
    with open(pem_name, "w") as pem_file:
        pem_file.write(private_pem)
        pass
    print("generate private pem: %s" % pem_name)
    pass

# make sign for zip_data with private key
pkey = M2Crypto.EVP.load_key_string(private_pem)
pkey.sign_init()
pkey.sign_update(zip_data)
sign = pkey.sign_final()

# generate public key DER 
if hasattr(key, "save_pub_key_der_bio"):
    mem_bio = M2Crypto.BIO.MemoryBuffer()
    key.save_pub_key_der_bio(mem_bio) # missing API on M2Crypto <= 0.20.2
    der_key = mem_bio.getvalue()
    pass
else:
    der_key = subprocess.Popen(
        ["openssl", "rsa", "-pubout", "-outform", "DER",
         "-inform", "PEM", "-in", pem_name],
        stdout=subprocess.PIPE).stdout.read()
    pass

# make crx
crx_name = dirname + ".crx"
magic = "Cr24"
version = struct.pack("<I", 2)
key_len = struct.pack("<I", len(der_key))
sign_len = struct.pack("<I", len(sign))
with open(crx_name, "w") as crx:
    crx.write(magic)
    crx.write(version)
    crx.write(key_len)
    crx.write(sign_len)
    crx.write(der_key)
    crx.write(sign)
    crx.write(zip_data)
    crx.flush()
    pass
print("update package: %s" % crx_name)
