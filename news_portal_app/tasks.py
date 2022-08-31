from celery import shared_task
import time
from django.core.mail import send_mail
from .models import Post


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task()
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task()
def send_my_mail():
    send_mail(subject="Новые статьи)",
              message=f"Еженедельная рассылка\n актуальные новости: {Post.heading}",
              from_email='****',
              recipient_list=['']
              )

#celery -A NewsPortal worker -l INFO -- запуск Celery через консоль