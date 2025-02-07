from django.db import models
from teacherProfile.models import Group

class Student(models.Model):
    record_book = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE,
        related_name='main_students'
    )  
    academic_score = models.PositiveIntegerField(default=0)
    research_score = models.PositiveIntegerField(default=0)
    sport_score = models.PositiveIntegerField(default=0)
    social_score = models.PositiveIntegerField(default=0)
    cultural_score = models.PositiveIntegerField(default=0)