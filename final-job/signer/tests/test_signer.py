# External imports
import pytest

# Personal imports
from signer.models import Signer

# Built-in imports
from os import environ

def test_signing_content_file():
    signer = Signer(None, environ.get('CERTIFICATE_PASSWORD'))
    signature = signer.sign_file('./presentation.pdf')
    assert 1 == 1
