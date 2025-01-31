import time
from typing import Any
import jwt
from django.conf import settings
from jwt import PyJWTError
import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")


def token_response(token: str):
    return {"access_token": token}


def token_response(token: str):
    """
    Helper function to structure the token response.
    """
    return {
        "access_token": token
    }


def signJWT(user_id: str, user_type: str) -> tuple[str, float]:
    """
    Function to generate a JWT token with user ID and user type, and an expiration date.
    """
    expiration_time = time.time() + 30 * 24 * 60 * 60  # 30 days expiration time
    payload = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": expiration_time
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token, expiration_time


def decodeJWT(token: str) -> dict[str, Any] | None:
    """
    Function to decode a JWT token and check if it's valid.
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Check if the token has expired
        if decoded_token.get("exp") and decoded_token["exp"] < time.time():
            return None

        # Check if necessary claims are present
        if "user_id" not in decoded_token or "user_type" not in decoded_token:
            return None

        return decoded_token
    except PyJWTError:
        return None
