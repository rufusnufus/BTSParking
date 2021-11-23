from typing import Optional

from fastapi import APIRouter, Cookie, HTTPException, Response, status

from app.core.security import create_access_code, verified_email
from app.models.user import User as ModelUser
from app.schemas.user import User, LoginCode
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
async def activate_login_link(login_code: LoginCode):
    email = await ModelUser.validate_magic_link(login_code.dict()["login_code"])
    if email:
        await ModelUser.delete_magic_link(email)
        cookie, _ = create_access_code(email)
        try:
            await ModelUser.set_cookie(email, cookie)
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
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get(
    "/me",
    summary="Return the information about the currently logged in user",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "User information returned successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "user-info": {
                            "summary": "user-info",
                            "value": {"email": "user@example.com", "is_admin": False},
                        },
                    }
                }
            },
        },
    },
)
async def get_user_info(AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await ModelUser.get_info(valid_email)
    return user


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
async def logout(AUTH_TOKEN: Optional[str] = Cookie(None)):
    valid_email = await ModelUser.check_cookie(AUTH_TOKEN)
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    await ModelUser.delete_cookie(AUTH_TOKEN)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie("AUTH_TOKEN", domain="localhost")
    return response


# @router.delete("/user", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(user: User):
    await ModelUser.delete(**user.dict())
    return Response(status_code=status.HTTP_204_NO_CONTENT)
