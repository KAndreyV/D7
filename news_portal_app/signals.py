from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers
from .models import Post


# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        subject = 'Ура новая статья)'
    else:
        subject = 'Одна из статей твоей любимой категории изменилась)'
    mail_managers(
        subject='subject',
        message=instance.heading,
    )
    print(f'{instance.heading}')
