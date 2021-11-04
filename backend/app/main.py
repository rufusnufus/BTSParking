from typing import List, Optional

import os
import uvicorn
from app.models import Car as ModelCar, User as ModelUser
from app.schema import InputCar, OutputCar, User
from app.app import app
from fastapi import status, Response, Cookie
from dotenv import load_dotenv
from app.db import db
from twilio.twiml.messaging_response import MessagingResponse
import sendgrid
from sendgrid.helpers.mail import *
from hashlib import sha256
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))


@app.post("/request-magic-link")
async def send_magic_link(user: User):
    user_exists = await ModelUser.get(**user.dict())

    if not user_exists:
        await ModelUser.create(**user.dict())
    
    link_create_time = time.time()
    link_expire_time = time.time() + 60*5
    user_data = f"{user.dict()['email']}{link_create_time}"
    magicID = sha256(user_data.encode('utf-8')).hexdigest()
    magic_link = f"http://127.0.0.1:80/apply/{magicID}"

    updated_user = await ModelUser.set_magic_link(
        user.dict()['email'], 
        magicID,
        link_expire_time
    )
    # TODO: uncomment when frontend will be integrated with backend
    # sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    # from_email = Email(os.environ.get("FROM_EMAIL"))
    # to_email = To(email)
    # subject = "Sending login link for BTSParking service"
    # content = Content("text/html", f"<html><head></head><body>Hello! Click <a href=\"{magic_link}\">the following link</a> to login to BTSParking service.</body></html>")
    # mail = Mail(from_email, to_email, subject, content)
    # response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)
    return magic_link

@app.post("/activate-magic-link/{magicID}")
async def send_magic_link(magicID: str):
    email = await ModelUser.validate_magic_link(magicID)
    if email:
        await ModelUser.delete_magic_link(email)
        cookie = f"{email}{time.time()}"
        cookie = sha256(cookie.encode('utf-8')).hexdigest()
        try: 
            set_cookie = await ModelUser.set_cookie(email, cookie)
            response = Response(status_code=status.HTTP_204_NO_CONTENT)
            response.set_cookie(
                "BTSAuthorization",
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
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/logout", status_code = status.HTTP_204_NO_CONTENT)
async def logout(BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("BTSAuthorization", domain="localhost")
        return response
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

@app.delete("/user", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user: User):
    deleted_user = await ModelUser.delete(**user.dict())
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/cars")
async def create_car(car: InputCar, BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        car_id = await ModelCar.create(**car.dict(), email=valid_email)
        return {"id": car_id}
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/cars", response_model=List[OutputCar])
async def get_cars(BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        cars = await ModelCar.get_all(valid_email)
        return cars
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED) 

@app.delete("/cars/{car_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int, BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        deleted_car_id = await ModelCar.delete(car_id, valid_email)
        if deleted_car_id:
            assert deleted_car_id == car_id
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            # if user asks to get not his car
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    else: 
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED) 

@app.get("/cars/{car_id}", response_model=OutputCar)
async def get_car(car_id: int, BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        car = await ModelCar.get(car_id, valid_email)
        if car: 
            return OutputCar(**car).dict()
        else:
            # if user asks to get not his car
            return Response(status_code=status.HTTP_403_FORBIDDEN)
    else: 
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
