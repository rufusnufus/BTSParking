import os
import time
from hashlib import sha256

import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../.env"))


def create_access_code(email: str) -> tuple:
    link_create_time = time.time()
    link_expire_time = time.time() + 60 * 5
    user_data = f"{email}{link_create_time}"
    login_code = sha256(user_data.encode("utf-8")).hexdigest()
    return (login_code, link_expire_time)


def verified_email(email: str) -> bool:
    response = requests.get(
        os.environ.get("REAL_EMAIL_API_LINK"),
        params={"email": email},
        headers={"Authorization": "Bearer " + os.environ.get("REAL_EMAIL_API_KEY")},
    )
    response_status = response.json()["status"]
    return False if response_status == "invalid" else True

def cookie_is_none(auth_token: str) -> bool:
    return False if auth_token else True
