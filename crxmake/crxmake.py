#!/usr/bin/env python
# -*- mode: python coding: utf-8 -*-

"""
    crxmake
    ~~~~~~~

    building google chrome extension crx with commandline
    it is inspired by rubygem's crxmake
    requires: M2Crypto module (and "openssl" commandline)

    :copyright: (c) 2010 bellbind
    :license: pending, see LICENSE for more details.
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

MAGIC = "Cr24"
VERSION = struct.pack("<I", 2)

def rm_trailing_slash(d):
    """Removing trailing slash from directory name

    usage:
        >>> rm_trailing_slash('foo/bar/')
        'foo/bar'
    """
    return d[:-1] if d.endswith(os.path.sep) else d

def package(basedir, pem_key=None, magic=MAGIC, version=VERSION):
    """Create a chrome extension .crx package of a base directory

    params:
        basedir - the base directory where the application is located
    """
    if not os.path.isdir(basedir):
        raise IOError("Non-existant directory <%s>" % basedir)
    crxd = rm_trailing_slash(basedir)

    try:
        zipdata = zipdir(crxd)
    except IOError as e:
        raise e
    pem, key = create_privatekey(crxd)
    sig = sign(zipdata, pem)
    der = create_publickey(crxd, key)

    der_len = struct.pack("<I", len(der))
    sig_len = struct.pack("<I", len(sig))

    with open("%s.crx" % crxd, 'w') as crx:
        data = [magic, version, der_len, sig_len, der, sig, zipdata]
        for d in data:
            crx.write(d)

def zipdir(directory):
    """Create a .zip of the directory in memory and return its data"""
    zip_memory = io.BytesIO()
    with zipfile.ZipFile(zip_memory, "w", zipfile.ZIP_DEFLATED) as zf:
        def _rec_zip(path, parent=""):
            """utility method for recursively zipping"""
            for d in dircache.listdir(path):
                child = os.path.join(path, d)
                name = "%s/%s" % (parent, d)
                if os.path.isfile(child):
                    zf.write(child, name)
                if os.path.isdir(child):
                    _rec_zip(child, name)
        _rec_zip(directory, "")
        zf.close()
        zipdata = zip_memory.getvalue()
        return zipdata
    raise IOError("Failed to create zip")

def create_publickey(crxd, key):
    """generate public key DER"""
    if hasattr(key, "save_pub_key_der_bio"):
        mem_bio = M2Crypto.BIO.MemoryBuffer()
        key.save_pub_key_der_bio(mem_bio) # missing API on M2Crypto <= 0.20.2
        return mem_bio.getvalue()
    else:
        return subprocess.Popen(
            ["openssl", "rsa", "-pubout", "-outform", "DER",
             "-inform", "PEM", "-in", "%s.pem" % crxd],
            stdout=subprocess.PIPE).stdout.read()

def create_privatekey(path):
    """Create a private key PEM file"""
    pemfile = "%s.pem" % path
    if os.path.exists(pemfile):
        with open(pemfile, "r") as pf:
            key = M2Crypto.RSA.load_key(pemfile)
            pem = pf.read()
            return pem, key
    with open(pemfile, "w") as pf:
        key = M2Crypto.RSA.gen_key(1024, 65537, lambda: None)
        pem = key.as_pem(cipher=None)
        pf.write(pem)
        return pem, key

def sign(data, pem):
    """Sign a data with a key using M2Crypto wrapper for OpenSSL EVP
    API
    """
    pkey = M2Crypto.EVP.load_key_string(pem)
    pkey.sign_init()
    pkey.sign_update(data)
    signature = pkey.sign_final()
    return signature
