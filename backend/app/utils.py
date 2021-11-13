import os

import sendgrid
from dotenv import load_dotenv
from sendgrid.helpers.mail import Content, Email, Mail, To

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "./.env"))


def send_link_to_email(email, link) -> int:
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email(os.environ.get("FROM_EMAIL"))
    to_email = To(email)
    subject = "Sending login link for BTSParking service"
    content = Content(
        "text/html",
        f"""<html>
                <head>
                </head>
                <body>Hello! Click
                        <a href="{link}">the following link</a>
                        to login to BTSParking service.
                </body>
            </html>""",
    )
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code
