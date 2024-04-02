from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_registration_email(user_email, event_name):
    send_mail(
        'Inscrição em Evento',
        f'Você foi registrado para o evento "{event_name}".',
        'seu_email@gmail.com',
        [user_email],
        fail_silently=False,
    )

@shared_task
def send_change_event_email(user_email, event_name, new_time):
    send_mail(
        'Seu evento mudou',
        f'O evento "{event_name}" foi alterado para a hora {new_time}',
        'seu_email@gmail.com',
        [user_email],
        fail_silently=False,
    )

@shared_task
def send_cancelled_event_email(user_email, event_name):
    send_mail(
        'Seu evento mudou',
        f'O evento "{event_name}" foi cancelado',
        'seu_email@gmail.com',
        [user_email],
        fail_silently=False,
    )