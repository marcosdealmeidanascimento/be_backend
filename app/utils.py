from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.core.config import settings


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY,
                                   algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def send_simple_message(email, token):
    import smtplib
    from email.message import EmailMessage
    email_address = settings.MAIL_USERNAME
    password = settings.MAIL_PASSWORD
    msg = EmailMessage()
    msg['Subject'] = 'Password Reset'
    msg['From'] = "LogBook App"
    msg['to'] = email['email']
    msg.set_content(
        f"""\
            A password reset was requested. If you didn't requested, no further action is needed.

            To reset your password click the link below:
            http://127.0.0.1/reset-password?{token}&tk={token}

        """
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, password)
        smtp.send_message(msg=msg)


def send_confirmation(email, token):
    import smtplib
    from email.message import EmailMessage
    email_address = settings.MAIL_USERNAME
    password = settings.MAIL_PASSWORD
    print(email)
    msg = EmailMessage()
    msg['Subject'] = 'Confirm Registration'
    msg['From'] = "LogBook App"
    msg['to'] = email
    msg.set_content(
        f"""\
            Almost there, to confirm your account follow the steps below. If you didn't requested, no further action is needed.

            To confirm your account click the link below:
            http://127.0.0.1/confirm?{token}&tk={token}

        """
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, password)
        smtp.send_message(msg=msg)