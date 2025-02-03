from django import forms
from .models import StudentDocument
from django.core.exceptions import ValidationError
class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['document', 'description', 'category']



def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Можно загружать только PDF-файлы!")

class StudentDocumentForm(forms.ModelForm):
    document = forms.FileField(validators=[validate_pdf])

    class Meta:
        model = StudentDocument
        fields = ['document', 'description', 'category']
