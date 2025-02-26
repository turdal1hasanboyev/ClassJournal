from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone_number', 'avatar', 'date_of_birth']


class SubjectSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'), write_only=True, source='teacher')

    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher', 'teacher_id', 'description', 'created_at']


class ClassroomSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)
    subjects_ids = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True, many=True, source='subjects')
    class_teacher = UserSerializer(read_only=True)
    class_teacher_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'), write_only=True, source='class_teacher')

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'subjects', 'subjects_ids', 'class_teacher', 'class_teacher_id', 'year', 'schedule']


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'), write_only=True, source='user')
    parent = UserSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='parent'), write_only=True, source='parent', required=False, allow_null=True)
    classroom = ClassroomSerializer(read_only=True)
    classroom_id = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), write_only=True, source='classroom')

    class Meta:
        model = Student
        fields = ['id', 'user', 'user_id', 'classroom', 'classroom_id', 'parent', 'parent_id', 'date_joined']


class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, source='student')
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True, source='subject')

    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_id', 'subject', 'subject_id', 'grade', 'comment', 'date_given']


class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, source='student')
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True, source='subject')

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_id', 'subject', 'subject_id', 'date', 'time', 'status', 'reason']


class HomeworkSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True, source='subject')
    assigned_by = UserSerializer(read_only=True)
    assigned_by_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='teacher'), write_only=True, source='assigned_by')

    class Meta:
        model = Homework
        fields = ['id', 'subject', 'subject_id', 'assigned_by', 'assigned_by_id', 'description', 'due_date', 'file']


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer(read_only=True)
    homework_id = serializers.PrimaryKeyRelatedField(queryset=Homework.objects.all(), write_only=True, source='homework')
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True, source='student')

    class Meta:
        model = HomeworkSubmission
        fields = ['id', 'homework', 'homework_id', 'student', 'student_id', 'submission_date', 'file', 'comment']


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    recipient_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='recipient')

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'recipient_id', 'title', 'message', 'created_at', 'is_read']
