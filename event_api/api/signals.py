from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import Event
from .tasks.send_email_tasks import send_change_event_email, send_cancelled_event_email


@receiver(post_save, sender=Event)
def event_updated(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return

    for registrations in instance.eventregistration_set.all():
        send_change_event_email.delay(user_email=registrations.user.email, event_name=instance.name, new_time=instance.time)


@receiver(pre_delete, sender=Event)
def event_cancelled(sender, instance, **kwargs):
    for registrations in instance.eventregistration_set.all():
        send_cancelled_event_email.delay(user_email=registrations.user.email, event_name=instance.name)
