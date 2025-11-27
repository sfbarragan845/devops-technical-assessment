"""
DevOps Microservice - REST API
Banco Pichincha Technical Assesment
"""
from flask import Flask, request, jsonify
import os

app = Flask(__name__)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)