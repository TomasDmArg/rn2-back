from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = os.getenv("SECRET_KEY")

    def __init__(self):
        if not self.secret:
            raise ValueError("SECRET_KEY is not set in the environment variables")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=30),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)