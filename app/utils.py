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
        f"""
        <!DOCTYPE html>
            <html>
                <head>
                    <link rel="preconnect" href="https://fonts.googleapis.com" />
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
                    <link
                    href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100;0,9..40,200;0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;0,9..40,900;0,9..40,1000;1,9..40,100;1,9..40,200;1,9..40,300;1,9..40,400;1,9..40,500;1,9..40,600;1,9..40,700;1,9..40,800;1,9..40,900;1,9..40,1000&display=swap"
                    rel="stylesheet"
                    />
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style type="text/css">"""+"""
                        * {
                            background-color: #000;
                            color: #fff;
                        }
                    """+"""
                    </style>
                </head>
                <body style="width: 100%;">
                    <div style="text-align: center; height: 50vh;">
                        <div>
                            <p style="font-weight: 900; font-size: 8rem;">be</p>
                            <p style="font-weight: 400; font-size: 4rem;">Alteração de senha</p>
                            <p style="font-weight: 400; font-size: 2rem;">Para alterar a sua senha, clique no botão abaixo. Caso não tenha feito a solicitação, nenhuma ação é necessária.</p>
                            <a href="http://127.0.0.1/reset-password?{token}&tk={token}" style="margin-top: 75px; text-decoration: none; color: #fff; font-weight: 900; font-size: 2rem; background: #ffcd2e; color: #fff; border-radius: 3px; border-color: #ffcd2e; padding: 20px;">Alterar senha</a>
                        </div>
                            
                    </div>
                </body>
            </html>
        """
    , subtype='html')

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
        f"""
        <!DOCTYPE html>
            <html>
                <head>
                    <link rel="preconnect" href="https://fonts.googleapis.com" />
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
                    <link
                    href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100;0,9..40,200;0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;0,9..40,900;0,9..40,1000;1,9..40,100;1,9..40,200;1,9..40,300;1,9..40,400;1,9..40,500;1,9..40,600;1,9..40,700;1,9..40,800;1,9..40,900;1,9..40,1000&display=swap"
                    rel="stylesheet"
                    />
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style type="text/css">"""+"""
                        * {
                            background-color: #000;
                            color: #fff;
                        }
                    """+"""
                    </style>
                </head>
                <body style="width: 100%;">
                    <div style="text-align: center; height: 50vh;">
                        <div>
                            <p style="font-weight: 900; font-size: 8rem;">be</p>
                            <p style="font-weight: 400; font-size: 4rem;">Bem-vindo</p>
                            <p style="font-weight: 400; font-size: 2rem;">Obrigado por se registrar. Para confirmar sua conta, clique no link abaixo. Caso não tenha feito o cadastro, nenhuma ação é necessária</p>
                            <a href="http://127.0.0.1/confirm?{token}&tk={token}" style="margin-top: 75px; text-decoration: none; color: #fff; font-weight: 900; font-size: 2rem; background: #ffcd2e; color: #fff; border-radius: 3px; border-color: #ffcd2e; padding: 20px;">Confirmar conta</a>
                        </div>
                            
                    </div>
                </body>
            </html>
        """
    , subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, password)
        smtp.send_message(msg=msg)