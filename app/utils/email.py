import emails
from app.core.config import settings
from typing import Dict, Any

def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> bool:
    message = emails.Message(
        subject=subject_template,
        html=html_template,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL)
    )
    
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    return response.status_code == 250

async def send_verification_email(email_to: str, token: str) -> bool:
    verification_url = f"{settings.SERVER_HOST}/api/v1/auth/verify/{token}"
    subject = "Verify your email"
    html_template = f"""
        <p>Please verify your email by clicking on the link below:</p>
        <p><a href="{verification_url}">{verification_url}</a></p>
    """
    
    return send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=html_template,
    )