from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Group(models.Model):
    FACULTY_CHOICES = [
        ('EiEB', 'Экономика и экономическая безопасность'),
        ('IT', 'Информационные технологии'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    faculty = models.CharField(max_length=15, choices=FACULTY_CHOICES)
    course = models.PositiveSmallIntegerField()
    curator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Student(models.Model):
    record_book = models.CharField(max_length=25, unique=True)
    full_name = models.CharField(max_length=150)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)