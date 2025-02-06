from django.shortcuts import render

from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Student, Group

class TeacherDashboardView(View):
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

class AddStudentView(View):
    def post(self, request):
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id, curator=request.user)
        
        student = Student.objects.create(
            record_book=request.POST.get('record_book'),
            full_name=request.POST.get('full_name'),
            group=group
        )
        
        return JsonResponse({
            'id': student.id,
            'full_name': student.full_name,
            'record_book': student.record_book
        })

class StudentActionsView(View):
    def delete(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        if student.group.curator != request.user:
            return JsonResponse({'error': 'Forbidden'}, status=403)
        student.delete()
        return JsonResponse({'status': 'deleted'})
