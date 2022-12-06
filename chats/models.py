from django.db import models
from application import settings


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Chat(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="author_chat", null=True,
                               on_delete=models.SET_NULL, verbose_name="Автор")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="members_chat", null=True,
                                     verbose_name="Участники")
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, verbose_name="Категория",
                                 related_name="chat")
    channel = models.BooleanField(default=False, verbose_name="Канал?")

    class Meta:
        verbose_name = "Чат"
        verbose_name_plural = "Чаты"


class Files(models.Model):
    path = models.CharField(max_length=200, verbose_name="Путь")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"


class Messages(models.Model):
    chat = models.ForeignKey(Chat, null=True, on_delete=models.SET_NULL, verbose_name="Чат" ,
                             related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                               verbose_name="Отправитель", related_name="messages")
    content = models.TextField(verbose_name="Текст")
    date_create = models.DateTimeField(verbose_name="Время", auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Прочитано?")
    files = models.ManyToManyField(Files, null=True, verbose_name="Файлы", related_name="messages",  blank=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("-date_create",)
