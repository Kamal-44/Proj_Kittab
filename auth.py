from fastapi import HTTPException, Header
from fastapi.params import Header

API_KEY="chaicode"

def verify_apikey(x_api_key:str=Header()):
    """ Verify x api key passed is correct or not in headers"""
    if x_api_key != API_KEY :
        raise HTTPException(status_code=401,detail="Invalid x-api-key")

    return x_api_key