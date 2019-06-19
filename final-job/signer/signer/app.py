# External imports
from dotenv import load_dotenv
from flask import Flask
from flask import request

# Personal imports
from signer.models import Signer

load_dotenv()
app = Flask(__name__)
signer = Signer()

@app.route('/sign', methods=['POST'])
def sign():
	content = request.files.get('file').read()
	return signer.sign_content(content)
