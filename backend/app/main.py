from typing import List, Optional

import os
import uvicorn
from app.models import Car as ModelCar, User as ModelUser, Space
from app.schema import InputCar, OutputCar, User
from app.app import app
from fastapi import status, Response, Cookie
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import *
from hashlib import sha256
import time
import requests


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))


@app.post("/request-magic-link")
async def send_magic_link(user: User):
    response = requests.get(
    os.environ.get('REAL_EMAIL_API_LINK'),
    params = {'email': user.dict()['email']},
    headers = {'Authorization': "Bearer " + os.environ.get('REAL_EMAIL_API_KEY') })
    response_status = response.json()['status']
    if response_status == "invalid":
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    
    user_exists = await ModelUser.get(**user.dict())

    if not user_exists:
        await ModelUser.create(**user.dict())
    
    link_create_time = time.time()
    link_expire_time = time.time() + 60*5
    user_data = f"{user.dict()['email']}{link_create_time}"
    login_code = sha256(user_data.encode('utf-8')).hexdigest()
    magic_link = f"http://127.0.0.1:80/login?code={login_code}"

    updated_user = await ModelUser.set_magic_link(
        user.dict()['email'], 
        login_code,
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
    # Response(status_code=status.HTTP_204_NO_CONTENT)
    return magic_link

@app.post("/activate-magic-link/{login_code}")
async def send_magic_link(login_code: str):
    email = await ModelUser.validate_magic_link(login_code)
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
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/logout", status_code = status.HTTP_204_NO_CONTENT)
async def logout(BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        await ModelUser.delete_cookie(BTSAuthorization)
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

@app.get("/zones/{zone_id}/free-spaces")
async def get_cars(zone_id: int, BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        free_spaces = await Space.get_free_spaces(zone_id)

        json_free_spaces=[]
        for free_space in free_spaces:
            json_free_space = jsonable_encoder(free_space)

            json_free_space.pop('zone_id', None)
            json_free_space.pop('car_id', None)

            start_x = json_free_space.pop('start_x', None)
            start_y = json_free_space.pop('start_y', None)
            json_free_space['start'] = [start_x, start_y]

            end_x = json_free_space.pop('end_x', None)
            end_y = json_free_space.pop('end_y', None)
            json_free_space['end'] = [end_x, end_y]
            
            json_free_spaces.append(json_free_space)
        return json_free_spaces
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED) 

@app.post("/zones/{zone_id}/book")
async def book_space(zone_id: int, space_id: int, car_id: int, BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        free_space = await Space.check_free_space(space_id, zone_id)
        
        if not free_space:
            return Response(status_code=status.HTTP_306_RESERVED)
        
        booked_space = await Space.book_space(space_id, zone_id, car_id)
        
        if booked_space: 
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else: 
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/zones/{zone_id}/release")
async def book_space(zone_id: int, space_id: int, BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        free_space = await Space.check_free_space(space_id, zone_id)
        
        if free_space:
            return Response(status_code=status.HTTP_403_FORBIDDEN)
        
        # check whether user has his car on space which tries to release
        space = await Space.get_space(space_id, zone_id)
        if not space: 
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # check whether user has his car on space which tries to release
        user_car = await ModelCar.get(dict(space)["car_id"], valid_email)
        if not user_car:
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        freed_space = await Space.release_space(space_id, zone_id)
        
        if freed_space: 
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else: 
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED) 

@app.post("/cars", response_model=OutputCar)
async def create_car(car: InputCar, BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        created_car = await ModelCar.create(**car.dict(), email=valid_email)
        return OutputCar(**created_car).dict()
    else:
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/cars")
async def get_cars(BTSAuthorization: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(BTSAuthorization)
    if valid_email:
        cars = await ModelCar.get_all(valid_email)
        json_cars=[]
        for car in cars:
            json_car = jsonable_encoder(car)
            json_car.pop('email', None)
            json_cars.append(json_car)
        # return Response(status_code=status.HTTP_200_OK, content=json_cars)
        return json_cars
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
            # if user asks car that doesn't exist
            return Response(status_code=status.HTTP_404_NOT_FOUND)
    else: 
        # if user is not authorized
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
