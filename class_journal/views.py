from django.contrib.auth import get_user_model

from rest_framework import generics

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

from .serializers import (
    UserSerializer, SubjectSerializer, ClassroomSerializer,
    StudentSerializer, GradeSerializer, AttendanceSerializer,
    HomeworkSerializer, HomeworkSubmissionSerializer, NotificationSerializer
)

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


User = get_user_model()


# 📌 Foydalanuvchilar
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 📌 Fanlar
class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# 📌 Sinflar
class ClassroomListView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


# 📌 O‘quvchilar
class StudentListView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# 📌 Baholar
class GradeListView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


# 📌 Davomat
class AttendanceListView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


# 📌 Uy vazifalari
class HomeworkListView(generics.ListCreateAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer


class HomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer


# 📌 Uy vazifalari javoblari
class HomeworkSubmissionListView(generics.ListCreateAPIView):
    queryset = HomeworkSubmission.objects.all()
    serializer_class = HomeworkSubmissionSerializer


class HomeworkSubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HomeworkSubmission.objects.all()
    serializer_class = HomeworkSubmissionSerializer


# 📌 Bildirishnomalar
class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
