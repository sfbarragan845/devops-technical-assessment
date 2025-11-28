"""
DevOps Microservice - REST API
Banco Pichincha Technical Assesment
"""
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from app.auth import require_api_key

app = Flask(__name__)

# Load variables from .env
load_dotenv()

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables")

@app.route('/DevOps', methods=['POST'])
@require_api_key
def devops_endpoint():
    """
    Endpoint principal /DevOps
    Acept POST with JSON and returns personalized message.
    """
    data = request.get_json()
    to_name = data['to']
    
    response = {"message": f"Hello {to_name} your message will be send"}
    
    return jsonify(response), 200

@app.route('/DevOps', methods=['GET', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def devops_error():
    """
    Manage all requests methods not allowed.
    """
    return "Error", 405


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)