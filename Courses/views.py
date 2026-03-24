from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Course, Enrollment, CourseInstructor, Lesson
from .Serializers import (
    CourseSerializer, EnrollmentSerializer,
    CourseInstructorSerializer, LessonSerializer
)
from .permissions import IsAdminOrReadOnly, IsInstructorOfCourse, IsStudentOwnerOrAdmin


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]
    # No need for get_permissions() anymore — one clean permission class handles it


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOfCourse]

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        # Admins see all enrollments, students see only their own
        if self.request.user.is_staff:
            return Enrollment.objects.filter(course_id=course_id)
        return Enrollment.objects.filter(
            course_id=course_id,
            student=self.request.user  # ← students only see their own
        )

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(
            course_id=course_id,
            student=self.request.user  # ← fixed bug from before
        )


class CourseInstructorViewSet(viewsets.ModelViewSet):
    queryset = CourseInstructor.objects.all()
    serializer_class = CourseInstructorSerializer
    permission_classes = [IsAdminOrReadOnly]


class MyEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
