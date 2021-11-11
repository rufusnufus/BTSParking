from typing import Optional
import os
from fastapi import status, HTTPException, Response, Cookie
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import *
from hashlib import sha256
import time
import requests
from fastapi import APIRouter, HTTPException, status
from ..models import User as ModelUser
from ..schema import User

router = APIRouter(
    prefix="",
    tags=["Authorization"],
    responses={404: {"description": "Not found"}},
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))


@router.post("/request-login-link", summary="Generate a one-time link that will log a user in with their e-mail")
async def send_login_link(user: User):
    response = requests.get(
    os.environ.get('REAL_EMAIL_API_LINK'),
    params = {'email': user.dict()['email']},
    headers = {'Authorization': "Bearer " + os.environ.get('REAL_EMAIL_API_KEY') })
    response_status = response.json()['status']
    if response_status == "invalid":
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    user_exists = await ModelUser.get(**user.dict())

    if not user_exists:
        await ModelUser.create(**user.dict(), is_admin=False)
    
    email = user.dict()['email']
    link_create_time = time.time()
    link_expire_time = time.time() + 60*5
    user_data = f"{email}{link_create_time}"
    login_code = sha256(user_data.encode('utf-8')).hexdigest()
    magic_link = f"http://127.0.0.1:80/login?code={login_code}"

    updated_user = await ModelUser.set_magic_link(
        email, 
        login_code,
        link_expire_time
    )
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get("FROM_EMAIL"))
    to_email = To(email)
    subject = "Sending login link for BTSParking service"
    content = Content("text/html", f"<html><head></head><body>Hello! Click <a href=\"{magic_link}\">the following link</a> to login to BTSParking service.</body></html>")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/get-login-code", summary="Temporary endpoint to bypass e-mail and just get a login code")
async def get_login_code(user: User):
    # response = requests.get(
    # os.environ.get('REAL_EMAIL_API_LINK'),
    # params = {'email': user.dict()['email']},
    # headers = {'Authorization': "Bearer " + os.environ.get('REAL_EMAIL_API_KEY') })
    # response_status = response.json()['status']
    # if response_status == "invalid":
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The provided e-mail is invalid.")
    
    user_exists = await ModelUser.get(**user.dict())

    if not user_exists:
        await ModelUser.create(**user.dict(), is_admin=False)
    
    link_create_time = time.time()
    link_expire_time = time.time() + 60*5
    user_data = f"{user.dict()['email']}{link_create_time}"
    login_code = sha256(user_data.encode('utf-8')).hexdigest()

    updated_user = await ModelUser.set_magic_link(
        user.dict()['email'], 
        login_code,
        link_expire_time
    )
    return login_code

@router.post("/activate-login-link", summary="Perform authorization by a given one-time login code")
async def activate_login_link(login_code: str):
    email = await ModelUser.validate_magic_link(login_code)
    if email:
        await ModelUser.delete_magic_link(email)
        cookie = f"{email}{time.time()}"
        cookie = sha256(cookie.encode('utf-8')).hexdigest()
        try: 
            set_cookie = await ModelUser.set_cookie(email, cookie)
            response = Response(status_code=status.HTTP_204_NO_CONTENT)
            response.set_cookie(
                "AUTH_TOKEN",
                value=f"{cookie}",
                domain="localhost",
                httponly=True,
                max_age=43200,
                expires=43200,
            )
            return response
        except e: 
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/me", summary="Return the information about the currently logged in user", status_code=status.HTTP_200_OK)
async def get_user_info(AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The request is not authorized.")
    user = await ModelUser.get_info(valid_email)
    return user


@router.post("/logout", summary="Terminate a user's session", status_code = status.HTTP_204_NO_CONTENT)
async def logout(AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authorization cookie is provided")
    
    await ModelUser.delete_cookie(AUTH_TOKEN)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie("AUTH_TOKEN", domain="localhost")
    return response

# @router.delete("/user", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user: User):
    deleted_user = await ModelUser.delete(**user.dict())
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

