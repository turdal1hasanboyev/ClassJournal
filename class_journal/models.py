from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.role}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject)
    class_teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})
    year = models.IntegerField()
    schedule = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.year})"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='children', limit_choices_to={'role': 'parent'})
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    date_given = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[
                              ('present', 'Present'), ('absent', 'Absent')])
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    description = models.TextField()
    due_date = models.DateField()
    file = models.FileField(upload_to='homeworks/', blank=True, null=True)

    def __str__(self):
        return f"{self.subject} - {self.due_date}"


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to='homework_submissions/', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.homework}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.recipient}"
