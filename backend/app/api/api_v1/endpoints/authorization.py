from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (cookie_is_none, create_access_code,
                               oauth2_scheme, verified_email)
from app.models.user import User as ModelUser
from app.schemas.user import User
from app.utils import send_link_to_email

router = APIRouter()


@router.post(
    "/request-login-link",
    summary="Generate a one-time link that will log a user in with their e-mail",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "A login link is sent to the e-mail successfully.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "The provided e-mail is invalid.",
        },
    },
)
async def send_login_link(user: User):
    email = user.dict()["email"]
    if not verified_email(email):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    user_exists = await ModelUser.get(**user.dict())
    if not user_exists:
        await ModelUser.create(**user.dict(), is_admin=False)

    login_code, code_expire_time = create_access_code(email)
    magic_link = f"http://127.0.0.1:80/login?code={login_code}"

    await ModelUser.set_magic_link(email, login_code, code_expire_time)

    status_code = send_link_to_email(email, magic_link)
    if status_code == 202:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(
    "/get-login-code",
    summary="Temporary endpoint to bypass e-mail and just get a login code",
    responses={
        status.HTTP_200_OK: {
            "description": "A login code is returned successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "login-code": {
                            "summary": "login-code",
                            "value": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
                        },
                    }
                }
            },
        },
    },
)
async def get_login_code(user: User):
    user_exists = await ModelUser.get(**user.dict())

    if not user_exists:
        await ModelUser.create(**user.dict(), is_admin=False)

    email = user.dict()["email"]
    login_code, code_expire_time = create_access_code(email)

    await ModelUser.set_magic_link(email, login_code, code_expire_time)
    return login_code


@router.post(
    "/activate-login-link",
    summary="Perform authorization by a given one-time login code",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successful authorization.",
        },
    },
)
async def activate_login_link(form_data: OAuth2PasswordRequestForm = Depends()):
    email = await ModelUser.validate_magic_link(form_data.password)
    if email:
        await ModelUser.delete_magic_link(email)
        cookie, _ = create_access_code(email)
        try:
            await ModelUser.set_cookie(email, cookie)
            return {"token_type": "Bearer", "access_token": cookie}
        except e:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/logout",
    summary="Terminate a user's session",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Session terminated successfully.",
        },
    },
)
async def logout(auth_token: str = Depends(oauth2_scheme)):
    if cookie_is_none(auth_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    valid_email = await ModelUser.check_cookie(auth_token)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await ModelUser.delete_cookie(auth_token)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    return response


# @router.delete("/user", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user: User):
    await ModelUser.delete(**user.dict())
    return Response(status_code=status.HTTP_204_NO_CONTENT)
