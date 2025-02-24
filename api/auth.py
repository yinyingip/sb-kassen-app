from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import os

# Define the header name for the API Key
API_KEY_NAME = "API_KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

# The API key you want to validate
API_KEY = os.environ['API_KEY']

# Dependency function to check the API key
def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key