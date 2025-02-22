from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    patronymic = models.CharField("Отчество", max_length=150, blank=True)
    phone = models.CharField("Телефон", max_length=20)
    faculty = models.CharField("Факультет", max_length=100, blank=True)
    position = models.CharField("Должность", max_length=100, blank=True)
    email = models.EmailField("Email", blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()

    def get_full_name(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name.strip()
