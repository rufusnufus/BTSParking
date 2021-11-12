from fastapi import APIRouter, HTTPException, status, Response, Cookie
from fastapi.encoders import jsonable_encoder
from typing import Optional
from ..models import Car as ModelCar, User as ModelUser, Space
from ..exceptions import EXCEPTION_401


router = APIRouter(
    prefix="/zones",
    tags=["Booking"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{zone_id}/spaces", summary="List all the spaces in the zone along with the current occupying vehicles")
async def get_spaces(zone_id: int, AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email: 
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The request is not authorized.")
    
    is_admin = await ModelUser.is_admin(valid_email)
    if not is_admin: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="A non-admin user attempted to access this endpoint.")
    
    # TODO: create zone validation for 404 error, when zones table will be ready

    spaces = await Space.get_spaces(zone_id)
    json_spaces=[]
    for space in spaces:
        json_space = jsonable_encoder(space)

        json_space.pop('zone_id', None)
        if json_space['car_id'] == None:
            json_space.pop('car_id', None)

        start_x = json_space.pop('start_x', None)
        start_y = json_space.pop('start_y', None)
        json_space['start'] = [start_x, start_y]

        end_x = json_space.pop('end_x', None)
        end_y = json_space.pop('end_y', None)
        json_space['end'] = [end_x, end_y]
        
        json_spaces.append(json_space)
    return json_spaces

@router.get("/{zone_id}/free-spaces", summary="List the spaces that are available for parking")
async def get_free_spaces(zone_id: int, AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email: 
        # user is not authorized
        raise EXCEPTION_401
    
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
     

@router.post("/{zone_id}/book", summary="Book a parking space")
async def book_space(zone_id: int, space_id: int, car_id: int, AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email: 
        # user is not authorized
        raise EXCEPTION_401
    
    free_space = await Space.check_free_space(space_id, zone_id)
    if not free_space:
        raise HTTPException(status_code=status.HTTP_306_RESERVED)
    
    booked_space = await Space.book_space(space_id, zone_id, car_id)
    
    if booked_space: 
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/{zone_id}/release", summary="Stop occupying a parking space")
async def book_space(zone_id: int, space_id: int, AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email: 
        # user is not authorized
        raise EXCEPTION_401
    
    free_space = await Space.check_free_space(space_id, zone_id)
    if free_space:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    # check whether user has his car on space which tries to release
    space = await Space.get_space(space_id, zone_id)
    if not space: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # check whether user has his car on space which tries to release
    user_car = await ModelCar.get(dict(space)["car_id"], valid_email)
    if not user_car:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    freed_space = await Space.release_space(space_id, zone_id)
    if freed_space: 
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
