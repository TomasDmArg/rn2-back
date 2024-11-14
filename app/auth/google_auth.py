from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleAuth:
    def __init__(self):
        self.GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        if not self.GOOGLE_CLIENT_ID:
            raise ValueError("GOOGLE_CLIENT_ID is not set in environment variables")

    async def verify_google_token(self, token: str):
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.GOOGLE_CLIENT_ID
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            return {
                'email': idinfo['email'],
                'email_verified': idinfo['email_verified'],
                'name': idinfo.get('name'),
                'picture': idinfo.get('picture')
            }
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid Google token"
            ) 