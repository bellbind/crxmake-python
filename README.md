# crxmake-python

Python script for building google chrome extension crx package.
It is inspired by rubygems' crxmake.

## usage:

    crxmake.py PACKAGE_BASE_DIR

## requires:

- python 2
- M2Crypto
- "openssl" command: because current M2Crypto lacks func for rsa pubout DER

## appendix: m2crypto-0.20.2-enable-rsa-pubout.patch

"svn diff" output for appending the feature for rsa pubout DER.

Howto build m2crypto with it:

    svn co http://svn.osafoundation.org/m2crypto/tags/0.20.2 m2crypto-0.20.2
    cd m2crypto-0.20.2
    patch -p0 < ../m2crypto-0.20.2-enable-rsa-pubout.patch
    python setup.py build

