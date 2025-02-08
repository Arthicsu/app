from django.shortcuts import render
from django.db.models import F, Q, ExpressionWrapper, IntegerField
from teacherProfile.models import Group, Student

def student_rating(request):
    # Получение параметров
    category = request.GET.get('category', 'total')
    search = request.GET.get('search', '')
    faculty = request.GET.get('faculty', '')
    course = request.GET.get('course', '')
    group = request.GET.get('group', '')
    sort = request.GET.get('sort', '')
    order = request.GET.get('order', 'desc')

    # Маппинг категорий на поля сортировки (по убыванию)
    category_sort_mapping = {
        'total': '-calculated_total',
        'academic': '-academic_score',
        'research': '-research_score',
        'sport': '-sport_score',
        'social': '-social_score',
        'cultural': '-cultural_score',
        'full_name': 'full_name'
    }

    # Определение поля сортировки
    if sort:
        sort_field = f'-{sort}' if order == 'desc' else sort
    else:
        sort_field = category_sort_mapping.get(category, '-calculated_total')

    # Аннотирование общего рейтинга
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

    # Фильтрация
    if search:
        queryset = queryset.filter(
            Q(full_name__icontains=search) | 
            Q(record_book__icontains=search)
        )
    
    if faculty:
        queryset = queryset.filter(group__faculty=faculty)
    
    if group:
        queryset = queryset.filter(group__name=group)

    # Сортировка по убыванию баллов
    queryset = queryset.order_by(sort_field)

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
        'faculties': Group.FACULTY_CHOICES,
        'groups': Group.objects.all(),
        'search': search,
        'score_field': 'calculated_total' if category == 'total' else f'{category}_score'
    }

    if request.headers.get('HX-Request'):
        return render(request, 'main/partials/student_table.html', context)

    return render(request, 'main/index.html', context)