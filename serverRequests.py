from datetime import datetime
import json

import jwt
from fastapi import HTTPException

import requests

from config import API_URL, PORTAL_ID, JWT_SECRET_KEY, ALGORITHM


def verify_token(authToken: str, token: str):
    headers = {"Authorization": "Bearer " + authToken, "Accept": "application/json", "Content-Type": "application/json"}
    # headers = {"Accept": "application/json", "Content-Type": "application/json"}

    content = {"token": token,
               "portal_id": PORTAL_ID
               }
    body = json.dumps(content)

    response = requests.post(url=API_URL + "/user/verify", data=body, headers=headers)
    responseJson = response.json()
    return responseJson['code']


def get_token_info(authToken: str, token: str):
    text_response = []
    headers = {"Authorization": "Bearer " + authToken, "Accept": "application/json", "Content-Type": "application/json"}
    if token:
        content = {"token": token,
                   "portal_id": PORTAL_ID
                   }
        body = json.dumps(content)
        if verify_token(authToken, token) == "200":
            text = ""
            response = (requests.post(url=API_URL + "/user/userInfo", data=body, headers=headers))
            response = response.json()
            print(response)
            information = response['result']
            for clave in information:
                valor = information[clave]
                text_response.append(clave+": "+valor)
            print(text_response)
            return text_response
        else:
            text_response.append("Token no Valido")
            return text_response
    text_response.append("Error al leer QR")
    text_response.append("Vuelva a intentar")
    return text_response


def login():
    contents = open('loginBody.json', 'rb').read()
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url=API_URL + "/user/login", data=contents, headers=headers)
    return response.json()
