"""
JWT Manager
Manage creation and validation of JSON Web Tokens (JWT)
"""

import jwt
import os
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

class JWTManager:
    """
    JWT Manager class to handle JWT creation and validation
    """
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET')
        if not self.secret_key:
            raise ValueError("JWT_SECRET debe estar configurado en las variables de entorno")

        self.algorithm = 'HS256'
        self.expiration_hours = 1
    
    def generate_token(self, user_id=None):
        """
        Generate a JWT token unique for each request
        
        Args:
            user_id (str): Optional user identifier to include in the token payload
        Returns:
            str: Encoded JWT token
        """
        if user_id is None:
            user_id = str(uuid.uuid4())
        
        jti = str(uuid.uuid4())
        
        payload = {
            'user_id': user_id,
            'jti': jti,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.expiration_hours)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        return token
    
    def verify_token(self, token):
        """
        Verify a JWT token
        
        Args:
            token (str): JWT token to verify
        Returns:
            dict: Decoded token payload if valid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            # Token expirado
            return None
        
        except jwt.InvalidTokenError:
            # Token inválido
            return None
        
    def is_token_valid(self, token):
        """
        Check if a JWT token is valid
        
        Args:
            token (str): JWT token to check
        Returns:
            bool: True if valid, False otherwise
        """
        return self.verify_token(token) is not None