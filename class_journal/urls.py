from django.urls import path

from .views import RegisterView, LogoutView

from .views import (
    UserListView, UserDetailView, 
    SubjectListView, SubjectDetailView, 
    ClassroomListView, ClassroomDetailView, 
    StudentListView, StudentDetailView, 
    GradeListView, GradeDetailView, 
    AttendanceListView, AttendanceDetailView,
    HomeworkListView, HomeworkDetailView, 
    HomeworkSubmissionListView, HomeworkSubmissionDetailView, 
    NotificationListView, NotificationDetailView,
)

urlpatterns = [
    # Foydalanuvchilar (O‘qituvchi, O‘quvchi, Ota-ona)
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Fanlar
    path('subjects/', SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject-detail'),

    # Sinflar
    path('classrooms/', ClassroomListView.as_view(), name='classroom-list'),
    path('classrooms/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),

    # O‘quvchilar
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Baholar
    path('grades/', GradeListView.as_view(), name='grade-list'),
    path('grades/<int:pk>/', GradeDetailView.as_view(), name='grade-detail'),

    # Davomat
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/<int:pk>/', AttendanceDetailView.as_view(), name='attendance-detail'),

    # Uy vazifalari
    path('homeworks/', HomeworkListView.as_view(), name='homework-list'),
    path('homeworks/<int:pk>/', HomeworkDetailView.as_view(), name='homework-detail'),

    # Uy vazifasi javoblari
    path('homework-submissions/', HomeworkSubmissionListView.as_view(), name='homework-submission-list'),
    path('homework-submissions/<int:pk>/', HomeworkSubmissionDetailView.as_view(), name='homework-submission-detail'),

    # Bildirishnomalar
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),

    path('register/', RegisterView.as_view(), name='register'),  # Register
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout
]
