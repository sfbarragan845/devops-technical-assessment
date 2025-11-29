"""
DevOps Microservice - REST API
Banco Pichincha Technical Assesment
"""

from flask import Flask, request, jsonify
from functools import wraps
import os
from dotenv import load_dotenv
from app.auth import require_api_key, require_jwt
from app.jwt_manager import JWTManager

app = Flask(__name__)
jwt_manager = JWTManager()

# Load variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is not set in environment variables")


def validate_json_payload(f):
    """
    Decorator to validate JSON the JSON payload
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        required_fields = ["to", "from", "message", "timeToLifeSec"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        if not isinstance(data["message"], str):
            return jsonify({"error": "Field 'message' must be a string"}), 400
        if not isinstance(data["to"], str):
            return jsonify({"error": "Field 'to' must be a string"}), 400
        if not isinstance(data["from"], str):
            return jsonify({"error": "Field 'from' must be a string"}), 400
        if not isinstance(data["timeToLifeSec"], int):
            return jsonify({"error": "Field 'timeToLifeSec' must be an integer"}), 400

        return f(*args, **kwargs)

    return decorated_function


@app.route("/DevOps", methods=["POST"])
@require_api_key
@require_jwt
@validate_json_payload
def devops_endpoint():
    """
    Endpoint principal /DevOps
    Acept POST with JSON and returns personalized message.
    """
    data = request.get_json()
    to_name = data["to"]

    response = {"message": f"Hello {to_name} your message will be send"}

    return jsonify(response), 200


@app.route("/DevOps", methods=["GET", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
def devops_error():
    """
    Manage all requests methods not allowed.
    """
    return "ERROR", 405


@app.route("/generate-jwt", methods=["POST"])
@require_api_key
def generate_jwt():
    """
    Endpoint to generate a JWT token for testing purposes.
    Requires API key authentication.
    """
    data = request.get_json() or {}
    user_id = data.get("user_id", "test_user")

    token = jwt_manager.generate_token(user_id)
    return jsonify({"token": token}), 200


@app.route(
    "/generate-jwt", methods=["GET", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
def token_error():
    """
    Manage all requests methods not allowed.
    """
    return "ERROR", 405


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Kubernetes"""
    return jsonify({"status": "healthy"}), 200


@app.route("/ready", methods=["GET"])
def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    return jsonify({"status": "ready"}), 200


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors for undefined routes.
    """
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 internal server errors.
    """
    return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
