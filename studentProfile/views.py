from django.shortcuts import render, get_object_or_404
from teacherProfile.models import Student
import json

def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    achievements = student.student_documents.all().order_by('-uploaded_at')
    
    radar_data = [
        student.social_score,
        student.academic_score,
        student.sport_score,
        student.cultural_score,
        student.research_score
    ]
    
    context = {
        'student': student,
        'achievements': achievements,
        'radar_labels_json': json.dumps([
            "ОБЩЕСТВЕННАЯ ДЕЯТЕЛЬНОСТЬ",
            "УЧЕБНАЯ ДЕЯТЕЛЬНОСТЬ", 
            "СПОРТИВНАЯ ДЕЯТЕЛЬНОСТЬ",
            "КУЛЬТУРНО-ТВОРЧЕСКАЯ ДЕЯТЕЛЬНОСТЬ",
            "НАУЧНО-ИССЛЕДОВАТЕЛЬСКАЯ"
        ], ensure_ascii=False),
        'radar_data_json': json.dumps(radar_data)
    }
    return render(request, 'studentProfile/profile.html', context)