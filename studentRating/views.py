from django.shortcuts import render
from .models import StudentRating

def radar_chart_view(request):
    students = StudentRating.objects.all()
    
    labels = ["Учебная деятельность", "Научно-исследовательская деятельность", "Культурно-творческая", "Спортивная деятельность", "Общественная деятельность"]
    datasets = []

    for student in students:
        datasets.append({
            "label": student.student_name,
            "data": [student.competence_1, student.competence_2, student.competence_3, student.competence_4, student.competence_5],
            "borderColor": "rgba(54, 162, 235, 1)",
            "backgroundColor": "rgba(54, 162, 235, 0.2)"
        })

    context = {
        "title": "test",
        "labels": labels,
        "datasets": datasets,
    }

    return render(request, 'studentRating/chart.html', context)
