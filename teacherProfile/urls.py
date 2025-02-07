from django.urls import path
from . import views

app_name = 'teacherProfile'

urlpatterns = [
    path('profile/', views.TeacherProfileView.as_view(), name='teacher_profile'),
    path('api/students/add/', views.AddStudentView.as_view(), name='add_student'),
    path('api/groups/<int:group_id>/add/', views.GroupActionsView.as_view(), name='add_group'),
    path('api/groups/<int:group_id>/remove/', views.GroupActionsView.as_view(), name='remove_group'),
    path('api/students/<int:student_id>/delete/', views.StudentActionsView.as_view(), name='delete_student'),
]