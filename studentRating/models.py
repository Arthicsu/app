from django.db import models

class StudentRating(models.Model):
    student_name = models.CharField(max_length=255)
    competence_1 = models.IntegerField()
    competence_2 = models.IntegerField()
    competence_3 = models.IntegerField()
    competence_4 = models.IntegerField()
    competence_5 = models.IntegerField()

    def __str__(self):
        return self.student_name
