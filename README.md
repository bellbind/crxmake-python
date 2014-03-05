# crxmake-python

Python script for building google chrome extension crx package.
It is inspired by rubygems' crxmake.

## Ubuntu Installation

    sudo apt-get install swig
    sudo pip install crxmake

## Usage:

    crxmake.py PACKAGE_BASE_DIR

## Example

An example extension named 'app' is provided in the examples/
directory for testing purposes:

    $ crxmake.py examples/app
    $ ls examples/app
    $ app app.crx app.pem

## Requires:

- python 2
- swig
- M2Crypto (available via pip, requires swig)
- "openssl" command: because current M2Crypto lacks func for rsa pubout DER

## Legacy Dependencies

### Appendix: m2crypto-0.20.2-enable-rsa-pubout.patch

"svn diff" output for appending the feature for rsa pubout DER.

Howto build m2crypto with it:

    svn co http://svn.osafoundation.org/m2crypto/tags/0.20.2 m2crypto-0.20.2
    cd m2crypto-0.20.2
    patch -p0 < ../legacy/m2crypto-0.20.2-enable-rsa-pubout.patch
    python setup.py build

(I hope someone send it to M2Crypto maintainer ^^)

## Resources:

- "M2Crypto":http://chandlerproject.org/bin/view/Projects/MeTooCrypto
- "crxmake":http://github.com/Constellation/crxmake
- "Packing Chrome extensions in Python":http://grack.com/blog/2009/11/09/packing-chrome-extensions-in-python/
