from django.db import models
from teacherProfile.models import Student

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('social', 'Общественная деятельность'),
        ('academic', 'Учебная деятельность'),
        ('sport', 'Спортивная деятельность'),
        ('cultural', 'Культурно-творческая деятельность'),
        ('research', 'Научно-исследовательская'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    achievement = models.CharField(max_length=255)
    score = models.PositiveIntegerField()
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.achievement} ({self.category})"