from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that inherits from AbstractUser.
    """

    ROLE_CHOICES = (
        ('teacher', ('Teacher')),
        ('student', ('Student')),
        ('parent', ('Parent')),
        ('admin', ('Admin')),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True, db_index=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} - {self.role}"


class Subject(models.Model):
    """
    Model for subjects.
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f"{self.name}"


class Classroom(models.Model):
    """
    Model for classrooms.
    """

    name = models.CharField(max_length=50, unique=True, db_index=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    class_teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})
    year = models.IntegerField(default=0)
    schedule = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Classroom'
        verbose_name_plural = 'Classrooms'

    def __str__(self):
        return f"{self.name} ({self.year})"


class Student(models.Model):
    """
    Model for students.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    parent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               blank=True, related_name='children', limit_choices_to={'role': 'parent'})
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.user.username}"


class Grade(models.Model):
    """
    Model for grades.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    date_given = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade}"


class Attendance(models.Model):
    """
    Model for attendance.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[
                              ('present', 'Present'), ('absent', 'Absent')])
    reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class Homework(models.Model):
    """
    Model for homework.
    """

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to='homeworks/', blank=True, null=True)

    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

    def __str__(self):
        return f"{self.subject} - {self.due_date}"


class HomeworkSubmission(models.Model):
    """
    Model for homework submission.
    """

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to='homework_submissions/', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Homework Submission'
        verbose_name_plural = 'Homework Submissions'

    def __str__(self):
        return f"{self.student} - {self.homework}"


class Notification(models.Model):
    """
    Model for notification.
    """

    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, db_index=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.title} - {self.recipient}"
