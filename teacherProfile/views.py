from django.shortcuts import render

from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Student, Group

class TeacherProfileView(View):
    def get(self, request):
        curated_groups = Group.objects.filter(curator=request.user)
        selected_group = None
        faculty = request.GET.get('faculty')
        course = request.GET.get('course')
        
        if 'group' in request.GET:
            try:
                selected_group = curated_groups.get(id=request.GET['group'])
            except Group.DoesNotExist:
                pass
        
        if not selected_group and curated_groups.exists():
            selected_group = curated_groups.first()
        
        available_groups = Group.objects.filter(curator__isnull=True)
        if faculty:
            available_groups = available_groups.filter(faculty=faculty)
        if course:
            available_groups = available_groups.filter(course=course)
        
        students = Student.objects.filter(group=selected_group) if selected_group else []
        
        return render(request, 'teacherProfile/index.html', {
            'curated_groups': curated_groups,
            'selected_group': selected_group,
            'students': students,
            'available_groups': available_groups,
            'selected_faculty': faculty,
            'selected_course': course,
        })

class GroupActionsView(View):
    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        
        if 'add' in request.path:
            group.curator = request.user
            group.save()
        
        elif 'remove' in request.path:
            group.curator = None
            group.save()
        
        return JsonResponse({'status': 'ok'})

from django.db import IntegrityError

from django.http import JsonResponse
from django.views import View
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from .models import Student, Group

class AddStudentView(View):
    def post(self, request):
        try:
            # Получаем данные из формы
            group_id = request.POST.get('group_id')
            record_book = request.POST.get('record_book')
            full_name = request.POST.get('full_name')
            
            # Валидация обязательных полей
            if not all([group_id, record_book, full_name]):
                return JsonResponse(
                    {'error': 'Все поля обязательны для заполнения'}, 
                    status=400
                )

            # Проверка прав доступа
            group = Group.objects.get(id=group_id)
            if group.curator != request.user:
                raise PermissionDenied

            # Создание студента
            student = Student.objects.create(
                record_book=record_book,
                full_name=full_name,
                group=group
            )
            
            return JsonResponse({
                'id': student.id,
                'full_name': student.full_name,
                'record_book': student.record_book
            })

        except IntegrityError:
            return JsonResponse(
                {'error': 'Студент с таким номером зачётки уже существует'}, 
                status=400
            )
            
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': 'Группа не найдена'}, 
                status=404
            )
            
        except PermissionDenied:
            return JsonResponse(
                {'error': 'Нет прав для добавления в эту группу'}, 
                status=403
            )
            
        except Exception as e:
            return JsonResponse(
                {'error': f'Внутренняя ошибка сервера: {str(e)}'}, 
                status=500
            )
class StudentActionsView(View):
    def delete(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        if student.group.curator != request.user:
            return JsonResponse({'error': 'Forbidden'}, status=403)
        student.delete()
        return JsonResponse({'status': 'deleted'})
    

