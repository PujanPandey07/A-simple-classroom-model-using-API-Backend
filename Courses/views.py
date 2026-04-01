from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
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

    # exact match filters — ?published=true or ?published=false
    filterset_fields = ['published']

    # searches these fields — ?search=django
    search_fields = ['title', 'description']

    # sorting — ?ordering=price or ?ordering=-created_at
    ordering_fields = ['created_at', 'price', 'title']
    ordering = ['-created_at']  # default: newest first


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOfCourse]

    # search lessons by title or content — ?search=variables
    search_fields = ['title', 'content']

    # filter by order number — ?order=1
    filterset_fields = ['order']

    # sort by order or created date — ?ordering=order
    ordering_fields = ['order', 'created_at']
    ordering = ['order']  # default: show lessons in their correct order

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]

    # sort enrollments by date — ?ordering=-enrolled_at
    ordering_fields = ['enrolled_at']
    ordering = ['-enrolled_at']  # default: most recent first

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        if self.request.user.is_staff:
            return Enrollment.objects.filter(course_id=course_id)
        return Enrollment.objects.filter(
            course_id=course_id,
            student=self.request.user
        )

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(
            course_id=course_id,
            student=self.request.user
        )


class CourseInstructorViewSet(viewsets.ModelViewSet):
    queryset = CourseInstructor.objects.all()
    serializer_class = CourseInstructorSerializer
    permission_classes = [IsAdminOrReadOnly]

    # search by instructor qualification — ?search=phd
    search_fields = ['qualification']

    # filter by experience years — ?experience=5
    filterset_fields = ['experience']

    # sort by experience — ?ordering=-experience
    ordering_fields = ['experience']
    ordering = ['-experience']  # default: most experienced first


class MyEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
