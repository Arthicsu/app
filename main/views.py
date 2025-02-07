from django.shortcuts import render
from django.db.models import F, Q, ExpressionWrapper, IntegerField
from teacherProfile.models import Group, Student

def student_rating(request):
    category = request.GET.get('category', 'total')
    search = request.GET.get('search', '')
    faculty = request.GET.get('faculty')
    course = request.GET.get('course')
    group = request.GET.get('group')

    if category == 'total':
        sort_param = '-calculated_total'
    else:
        sort_param = f'-{category}_score'

    queryset = Student.objects.annotate(
        calculated_total=ExpressionWrapper(
            F('academic_score') + 
            F('research_score') + 
            F('sport_score') + 
            F('social_score') + 
            F('cultural_score'),
            output_field=IntegerField()
        )
    ).select_related('group')

    if search:
        queryset = queryset.filter(
            Q(full_name__icontains=search) |
            Q(record_book__icontains=search)
        )
    
    if faculty:
        queryset = queryset.filter(group__faculty=faculty)
    
    if course:
        queryset = queryset.filter(group__course=course)
    
    if group:
        queryset = queryset.filter(group__name=group)

    queryset = queryset.order_by(sort_param)

    context = {
        'students': queryset,
        'categories': {
            'total': 'Общий рейтинг',
            'academic': 'Учебная деятельность',
            'research': 'Научно-исследовательская',
            'sport': 'Спортивная',
            'social': 'Общественная',
            'cultural': 'Культурно-творческая'
        },
        'current_category': category,
        'current_sort': sort_param,
        'faculties': Student.FACULTY_CHOICES,
        'groups': Group.objects.all(),
        'search': search
    }
    
    return render(request, 'main/index.html', context)