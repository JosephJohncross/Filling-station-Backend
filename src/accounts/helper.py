from django.core.mail import EmailMessage
from django.conf import settings


def send_email(email, mail_subject, message):
    """Generic method for sending email"""

    to_email = email
    mail = EmailMessage(mail_subject, message, from_email="", to=[to_email])
    mail.content_subtype = "html"
    mail.send()
