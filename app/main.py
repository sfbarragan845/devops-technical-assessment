"""
DevOps Microservice - REST API
Banco Pichincha Technical Assesment
"""
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/DevOps', methods=['POST'])
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