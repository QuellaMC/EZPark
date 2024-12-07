# app/utils/email.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import settings
from typing import Optional
from datetime import timedelta
from app.utils.auth import create_access_token
import logging

logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str) -> None:
    """
    Sends an email using SMTP.
    """
    msg = MIMEMultipart()
    msg['From'] = settings.smtp_sender
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port) as server:
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(msg)
        logger.info(f"Email sent to {to_email} with subject '{subject}'")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise Exception(f"Failed to send email: {e}")

def send_verification_email(to_email: str, user_id: int) -> None:
    """
    Sends a verification email to the user with a verification link.
    """
    try:
        verification_token = create_verification_token(user_id)
        logger.debug(f"Verification token created for user_id {user_id}: {verification_token}")
    except Exception as e:
        logger.error(f"Failed to create verification token for user_id {user_id}: {e}")
        raise Exception(f"Failed to create verification token: {e}")

    verification_link = f"{settings.frontend_url}auth/verify-email?token={verification_token}"
    subject = "EZPark Email Verification"
    body = f"Hello,\n\nPlease verify your email by clicking on the following link:\n{verification_link}\n\nThank you!"
    send_email(to_email, subject, body)

def create_verification_token(user_id: int) -> str:
    """
    Creates a JWT token for email verification.
    """
    data = {"sub": f"verify_email:{user_id}"}
    token = create_access_token(data, expires_delta=timedelta(hours=24))
    return token
