# External imports
from OpenSSL import crypto

# Built-in imports
from os import environ

class Signer(object):
	"""
	Class to model a signer of files. It uses a PKCS#12 certificate file to sign the
	content file. This class is able to sign only a content from file too.
	"""
	def __init__(self, certificate_path=None, certificate_password=None):
		"""
		In case of any of the parameters being None, will use default values to load variables
		for the certificate path and the password. Uses the OpenSSL library to load the content
		from the certificate file.

		:param certificate_path: String path to certificate file.
		:param certificate_password: String password used in the certificate password.
		:return: A Signer object
		"""
		cert_path = './cert.p12' if certificate_path is None else certificate_path
		cert_password = environ.get('CERTIFICATE_PASSWORD') if certificate_password is None else certificate_password
		cert_password_bytes = cert_password.encode()
		certificate_file = open(cert_path, 'rb').read()
		self.p12 = crypto.load_pkcs12(certificate_file, cert_password_bytes)
		self.pkey = self.p12.get_privatekey()
		self.cert = self.p12.get_certificate()

	def sign_file(self, file_path):
		"""
		Signs a file and returns its signature.
		:param file_path: Path to the file that will be signed
		:return: The file signature
		"""
		data = open(file_path, 'rb').read()
		return self.sign_content(data)

	def sign_content(self, content):
		"""
		Signs the content and returns its signature
		:param content: Content from file that will be signed
		:return: The file signature
		"""
		return crypto.sign(self.pkey, content, environ.get('DIGEST'))
