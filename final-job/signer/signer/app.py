# External imports
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

# Personal imports
from signer.models import Signer

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
signer = Signer()

@app.route('/sign', methods=['POST'])
def sign():
	content = request.files.get('file').read()
	return jsonify(signature=signer.sign_content(content).decode('ISO-8859-1'))
