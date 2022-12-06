from application.celery_conf import app
from django.core.mail import send_mail
from application.settings import EMAIL_HOST_USER
from chats.models import Messages
from django.db.models import Q
from chats.utils import publish_message


@app.task()
def task_publish(text):
    publish_message(text)


@app.task(time_limit=60)
def send_email(email, chat):
    send_mail(
        subject="User add",
        message="Chat "+str(chat)+": add user",
        from_email=EMAIL_HOST_USER,
        recipient_list=email
    )


@app.task
def send_no_read_message():
    for message in Messages.objects.filter(is_read=False):
        send_mail(
            subject="No read message",
            message=message.content,
            from_email=EMAIL_HOST_USER,
            recipient_list=list(message.chat.members.filter(~Q(id=message.sender.id)).values_list('email', flat=True))
        )
