from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_code, oauth2_scheme, verified_email
from app.logs import logger
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
    logger.info(f"function: send_login_link, params: {user}")
    email = user.dict()["email"]
    if not verified_email(email):
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    user_exists = await ModelUser.get(**user.dict())
    if not user_exists:
        logger.info(f"function: send_login_link, creating new user: {email}, not admin")
        await ModelUser.create(**user.dict(), is_admin=False)
        logger.info(f"function: send_login_link, created new user: {email}, not admin")

    code, code_expire_time = create_access_code(email, 60 * 5)
    logger.debug(
        f"function: send_login_link, code: {code}, code_expire_time: {code_expire_time}"
    )
    logger.info(f"function: send_login_link, generating magic link")
    magic_link = f"http://127.0.0.1:80/login?code={code}"

    await ModelUser.set_magic_link(email, code, code_expire_time)
    logger.info(f"function: send_login_link, magic link for {email} is set")
    logger.info(f"function: send_login_link, sending magic link to {email}")
    status_code = send_link_to_email(email, magic_link)
    logger.info(f"function: send_login_link, send_link_to_email's status_code: {status_code}")
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
    logger.info(f"function: get_login_code, params: {user}")
    user_exists = await ModelUser.get(**user.dict())
    if not user_exists:
        logger.info(f"function: get_login_code, creating new user: {user}, not admin")
        await ModelUser.create(**user.dict(), is_admin=False)
        logger.info(f"function: get_login_code, created new user: {user}, not admin")

    email = user.dict()["email"]
    code, code_expire_time = create_access_code(email, 60 * 5)
    
    await ModelUser.set_magic_link(email, code, code_expire_time)
    logger.info(f"function: get_login_code, login code for {email} is set")
    return code


@router.post(
    "/activate-login-code",
    summary="Perform authorization by a given one-time login code",
    responses={
        status.HTTP_200_OK: {
            "description": "Authorization token returned successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "token-response": {
                            "summary": "token-response",
                            "value": {
                                "token_type": "Bearer",
                                "access_token": "<token>",
                                "expires_in": 86400,
                                "user_info": {
                                    "email": "user@example.com",
                                    "is_admin": False,
                                },
                            },
                        },
                    }
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The link doesn't exist or isn't valid anymore.",
        },
    },
)
async def activate_login_code(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(
        f"function: activate_login_code, params: username = {form_data.username}, password = {form_data.password}"
    )
    email = await ModelUser.validate_magic_link(form_data.password)
    logger.info(f"function: activate_login_code, email: {email}")
    if email:
        await ModelUser.delete_magic_link(email)
        logger.info(f"function: activate_login_code, magic link is deleted for {email}")
        cookie, expires_in = create_access_code(email, 86400)
        logger.info(f"function: activate_login_code, cookie for {email} is created")
        user_info = await ModelUser.get_info(email)
        try:
            await ModelUser.set_cookie(email, cookie, expires_in)
            logger.info(f"function: activate_login_code, cookie for {email} is set")
            return {
                "token_type": "Bearer",
                "access_token": cookie,
                "expires_in": 86400,
                "user_info": user_info,
            }
        except Exception:
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
    valid_email = await ModelUser.check_cookie(auth_token)
    logger.info(f"function: logout, email: {valid_email}")
    if not valid_email:
        # user is not authorized
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    logger.info(f"function: logout, deleting cookie for {valid_email}")
    await ModelUser.delete_cookie(auth_token)
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    return response


# @router.delete("/user", status_code = status.HTTP_204_NO_CONTENT)
# async def delete_user(user: User):
#     await ModelUser.delete(**user.dict())
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
