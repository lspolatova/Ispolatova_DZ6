from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birthday = models.DateField(null=True, blank=True, verbose_name="День рождения")
    location = models.CharField(max_length=30, blank=True, verbose_name="Место нахождение")
    phone_number = models.CharField(max_length=30, blank=True, verbose_name="Номер телефона")
    hide_information = models.BooleanField(default=False, blank=True, verbose_name="Скрыть информацию?")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"