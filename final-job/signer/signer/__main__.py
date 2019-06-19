# External imports
from dotenv import load_dotenv
from OpenSSL import crypto

# Personal imports
from signer.app import app

# Built-in imports
from os import environ

if __name__ == '__main__':
	load_dotenv()
	app.run(host=environ.get('HOST'), port=environ.get('PORT'), debug=eval(environ.get('DEBUG')))
