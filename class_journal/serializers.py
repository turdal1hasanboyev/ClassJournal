from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import (
    Subject,
    Classroom,
    Student,
    Grade,
    Attendance,
    Homework,
    HomeworkSubmission,
    Notification,
)


User = get_user_model()


# 📌 Foydalanuvchilar (o‘qituvchi, o‘quvchi, ota-ona)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'role']


# 📌 Fanlar (Matematika, Informatika va h.k.)
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher']


# 📌 Sinflar (5-A, 6-B va h.k.)
class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'grade_level', 'teacher']


# 📌 O‘quvchilar (Har bir sinfga bog‘langan o‘quvchilar)
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user', 'classroom', 'parent_contact']


# 📌 Baholar (O‘quvchilarga qo‘yilgan baholar)
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'subject', 'score', 'date_given']


# 📌 Davomat (O‘quvchilarning darsga qatnashishi)
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'status']


# 📌 Uy vazifalari (O‘qituvchilar tomonidan berilgan vazifalar)
class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['id', 'subject', 'title', 'description', 'due_date']


# 📌 Uy vazifalari javoblari (O‘quvchilar topshirgan vazifalar)
class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSubmission
        fields = ['id', 'homework', 'student', 'file', 'submitted_at']


# 📌 Bildirishnomalar (O‘qituvchilardan ota-onalarga va o‘quvchilarga xabarlar)
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'message', 'created_at']
