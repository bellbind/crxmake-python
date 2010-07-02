# crxmake-python

Python script for building google chrome extension crx package.
It is inspired by rubygems' crxmake.

## Usage:

    crxmake.py PACKAGE_BASE_DIR

## Requires:

- python 2
- M2Crypto
- "openssl" command: because current M2Crypto lacks func for rsa pubout DER

## Appendix: m2crypto-0.20.2-enable-rsa-pubout.patch

"svn diff" output for appending the feature for rsa pubout DER.

Howto build m2crypto with it:

    svn co http://svn.osafoundation.org/m2crypto/tags/0.20.2 m2crypto-0.20.2
    cd m2crypto-0.20.2
    patch -p0 < ../m2crypto-0.20.2-enable-rsa-pubout.patch
    python setup.py build

(I hope someone send it to M2Crypto maintainer ^^)

## Resources:

- "M2Crypto":http://chandlerproject.org/bin/view/Projects/MeTooCrypto
- "crxmake":http://github.com/Constellation/crxmake
- "Packing Chrome extensions in Python":http://grack.com/blog/2009/11/09/packing-chrome-extensions-in-python/
