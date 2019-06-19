# External imports
from OpenSSL import crypto
import pytest

# Personal imports
from signer.app import app
from signer.models import Signer

# Built-in imports
from os import environ

@pytest.fixture
def client():
	app.config['TESTING'] = True
	client = app.test_client()
	yield client

def test_sign_route(client):
	file_path = './teaching-plan.pdf'
	with open(file_path, 'rb') as f:
		content = f.read()
		# File was already read it , so it needs to fix the seek with the following method
		f.seek(0)
		data = dict(file=f)
		res = client.post('/sign', data=data)
		signer = Signer('./cert.p12', environ.get('CERTIFICATE_PASSWORD'))
		assert crypto.verify(signer.cert, res.data, content, environ.get('DIGEST')) == None
