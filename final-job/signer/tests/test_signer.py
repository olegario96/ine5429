# External imports
from OpenSSL import crypto
import pytest

# Personal imports
from signer.models import Signer

# Built-in imports
from os import environ

def test_signing_content_file():
    file_path = './teaching-plan.pdf'
    with open(file_path, 'rb') as f:
        signer = Signer('./cert.p12', environ.get('CERTIFICATE_PASSWORD'))
        signature = signer.sign_file(file_path)
        data = f.read()
        assert crypto.verify(signer.cert, signature, data, environ.get('DIGEST')) == None
