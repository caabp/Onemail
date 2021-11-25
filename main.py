from os import name
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

def res_model_accInfo():
    class response_200(BaseModel):
        class Config:
            schema_extra = {
                    "example": {
                        "status": "success",
                    }
                }

    class response_400(BaseModel):
        class Config:
            schema_extra = {
                "example": {
                    "status": "fail",
                    "message": "header must include 'Authorization' key"
                }
            }

    class response_401(BaseModel):
        class Config:
            schema_extra = {
                "example": {
                    "status": "fail",
                    "message": "no valid authtoken present"
                }
            }

    class response_500(BaseModel):
        class Config:
            schema_extra = {
                "example": {
                    "status": "fail",
                    "message": "can not connect to OneMail server, please try again"
                }
            }

    status = {
        200: {"model": response_200, "description": "OK"},
        400: {"model": response_400, "description": "Bad Request"},
        401: {"model": response_401, "description": "Unauthorized"},
        500: {"model": response_500, "description": "Internal Server Error"}
    }
    return status

def res_model_login():
    class response_200(BaseModel):
        class Config():
            schema_extra = {
                "example": {
                    "status": "success",
                    "message": "login success"
                }
            }

    class response_401(BaseModel):
        class Config:
            schema_extra = {
                "example": {
                    "status": "fail",
                    "message": "no valid authtoken present"
                }
            }

    class response_500(BaseModel):
        class Config():
            schema_extra = {
                "example": {
                    "status": "fail",
                    "message": "can not connect to Onemail server, please try again"
                }
            }

    status = {
        200: {"model": response_200, "description": "OK"},
        401: {"model": response_401, "description": "Unauthorized"},
        500: {"model": response_500, "description": "Internal Server Error"}
    }
    return(status)
    

class data_login_form(BaseModel):
  name: str
  password: str

class data_acc_info(BaseModel):
    authen: str
    name: str

@app.post("/api/login", responses = res_model_login(), summary="Login")
async def login(login: data_login_form):

  url = "https://demo-onemail.one.th:9071/service/admin/soap"

  account = login.name
  password = login.password

  payload = "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\"> \r\n    <soap:Body xmlns=\"urn:zimbraAdmin\"> \r\n    <AuthRequest name=\""+account+"\" password=\""+password+"\"></AuthRequest>\r\n    </soap:Body> \r\n</soap:Envelope>"

  response = requests.request("POST", url, data=payload)

#   print(response.text)
  return(response.text)


@app.post("/api/getAccountInfo", responses = res_model_accInfo(), summary="Get Account Information")
async def getAccountInfo(info: data_acc_info):

    authen = info.authen
    name = info.name
    
    url = "https://demo-onemail.one.th:9071/service/admin/soap"

    payload = "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\"> \r\n    <soap:Body xmlns=\"urn:zimbraAdmin\"> \r\n        <GetAccountRequest attrs = \"displayName,givenName,sn,zimbraCreateTimestamp,zimbraMailHost,zimbraAccountStatus,zimbraLastLogonTimestamp\">\r\n             <account by=\"name\">" + name + "</account>\r\n        </GetAccountRequest>\r\n    </soap:Body>\r\n</soap:Envelope>"

    headers = {
    'Content-Type': 'application/xml',
    'Cookie': 'ZM_ADMIN_AUTH_TOKEN=' + authen 
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)
    return(response.text)