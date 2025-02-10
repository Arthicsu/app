from django.core.validators import FileExtensionValidator
from django.db import models
from teacherProfile.models import Student

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Учебная'),
        ('cultural', 'Культурно-творческая'),
        ('social', 'Общественная'),
        ('sport', 'Спортивная'),
        ('research', 'Научно-исследовательская'),
    ]
    
    DOC_TYPE_CHOICES = [
        ('diploma', 'Диплом'),
        ('certificate', 'Сертификат'),
        ('other', 'Другое'),
    ]

    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name='student_documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    achievement = models.CharField(max_length=255)
    score = models.PositiveIntegerField()
    doc_type = models.CharField(
        max_length=20, 
        choices=DOC_TYPE_CHOICES, 
        default='other'
    )
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png']
        )],
        null=True,
        blank=True
    )