from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_email(email):
    send_mail(
        "Review",
        "Dear reviewer thanks for your review",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    return 'ok'



@shared_task
def send_daily_report():
    send_mail(
        "REPORT",
        "just a reminder",
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_SEND_TO],
        fail_silently=False,
    )   
    return "ok"