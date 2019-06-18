# External imports
from dotenv import load_dotenv
from OpenSSL import crypto

# Built-in imports
from os import environ

if __name__ == '__main__':
	load_dotenv()
	CERT_PASSWORD = environ.get('CERT_PASSWORD')
	certificate = open('./cert.p12', 'rb').read()
	p12 = crypto.load_pkcs12(certificate, 'B3astInBlack')
	pkey = p12.get_privatekey()
	cert = p12.get_certificate()
	data = open('./presentation.pdf', 'rb').read()
	signature = crypto.sign(pkey, data, 'sha256')
	print(crypto.verify(cert, signature, data, 'sha256'))
