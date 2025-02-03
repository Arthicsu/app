from django.db import models
from django.contrib.auth.models import User

class StudentDocument(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Учебная'),
        ('research', 'Научно-исследовательская'),
        ('social', 'Общественная'),
        ('sports', 'Спортивная'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='documents/')
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Проверено куратором
    score = models.PositiveIntegerField(null=True, blank=True)  # Баллы за достижение

    def __str__(self):
        return f"{self.student.username} - {self.get_category_display()} ({self.uploaded_at.date()})"
