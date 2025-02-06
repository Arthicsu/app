from django.urls import path
from teacherProfile import views

app_name = 'teacherProfile'  # Добавьте это

urlpatterns = [
    path('profile/', views.TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('api/add-student/', views.AddStudentView.as_view(), name='add_student'),
    path('api/groups/<int:group_id>/add/', views.GroupActionsView.as_view(), name='add_group'),
    path('api/groups/<int:group_id>/remove/', views.GroupActionsView.as_view(), name='remove_group'),
    path('api/students/<int:student_id>/delete/', views.StudentActionsView.as_view(), name='delete_student'),
]
