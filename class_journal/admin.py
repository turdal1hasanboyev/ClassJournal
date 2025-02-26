from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    Subject,
    Classroom,
    Student,
    Grade,
    Attendance,
    Homework,
    HomeworkSubmission,
    Notification,
)


# Custom User modeli
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role',
                    'phone_number', 'date_of_birth', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        ('Qo‘shimcha ma’lumotlar', {
         'fields': ('role', 'phone_number', 'date_of_birth', 'avatar')}),
    )


# Fan modeli
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'created_at')
    search_fields = ('name', 'teacher__username')
    list_filter = ('teacher',)


# Sinf modeli
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_teacher', 'year')
    search_fields = ('name', 'class_teacher__username')
    list_filter = ('year',)


# O‘quvchi modeli
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom', 'parent', 'date_joined')
    search_fields = ('user__username', 'classroom__name', 'parent__username')


# Baholar modeli
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'grade', 'date_given')
    search_fields = ('student__user__username', 'subject__name')
    list_filter = ('subject', 'grade')


# Davomat modeli
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status')
    search_fields = ('student__user__username', 'subject__name')
    list_filter = ('date', 'status')


# Uy vazifalari modeli
@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'assigned_by', 'due_date')
    search_fields = ('subject__name', 'assigned_by__username')
    list_filter = ('due_date',)


# Uy vazifalari javoblari modeli
@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submission_date')
    search_fields = ('homework__subject__name', 'student__user__username')


# Bildirishnomalar modeli
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'created_at', 'is_read')
    search_fields = ('title', 'recipient__username')
    list_filter = ('is_read', 'created_at')
