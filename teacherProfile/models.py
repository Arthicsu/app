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
    curator = models.ForeignKey(User, on_delete=models.SET_NULL, 
                               null=True, blank=True,
                               related_name='curated_groups')

class Student(models.Model):
    FACULTY_CHOICES = [
        ('EiEB', 'Экономика и экономическая безопасность'),
        ('IT', 'Информационные технологии'),
    ]

    record_book = models.CharField(max_length=25, unique=True)
    full_name = models.CharField(max_length=150)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    academic_score = models.PositiveIntegerField(default=0)
    research_score = models.PositiveIntegerField(default=0)
    sport_score = models.PositiveIntegerField(default=0)
    social_score = models.PositiveIntegerField(default=0)
    cultural_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_score(self):
        return sum([
            self.academic_score,
            self.research_score,
            self.sport_score,
            self.social_score,
            self.cultural_score
        ])

    def get_score_by_category(self, category):
        return getattr(self, f'{category}_score', 0)