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


from django.core.cache import cache
from django.conf import settings


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related(
        'lessons', 'enrollments', 'instructors'
    ).all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['published']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'title']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        # Create a unique cache key based on the request query params
        # This way ?search=django and ?search=python have different caches
        cache_key = f'courses_list_{request.query_params}'

        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)  # return immediately, no database hit

        # Not in cache — get from database the normal way
        response = super().list(request, *args, **kwargs)

        # Store in cache for next time
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)

        return response

    def perform_create(self, serializer):
        # When a new course is created, clear the cache so the list is fresh
        serializer.save()
        cache.delete_pattern('courses_list_*')

    def perform_update(self, serializer):
        # When a course is updated, clear the cache
        serializer.save()
        cache.delete_pattern('courses_list_*')

    def perform_destroy(self, instance):
        # When a course is deleted, clear the cache
        instance.delete()
        cache.delete_pattern('courses_list_*')


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOfCourse]
    search_fields = ['title', 'content']
    filterset_fields = ['order']
    ordering_fields = ['order', 'created_at']
    ordering = ['order']

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        # select_related because each lesson belongs to ONE course
        return Lesson.objects.select_related('course').filter(
            course_id=course_id
        )

    def perform_create(self, serializer):
        serializer.save(course_id=self.kwargs['course_pk'])


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudentOwnerOrAdmin]
    ordering_fields = ['enrolled_at']
    ordering = ['-enrolled_at']

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        # select_related because each enrollment belongs to ONE student and ONE course
        base_queryset = Enrollment.objects.select_related(
            'student', 'course'
        ).filter(course_id=course_id)

        if self.request.user.is_staff:
            return base_queryset
        return base_queryset.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            course_id=self.kwargs['course_pk'],
            student=self.request.user
        )


class CourseInstructorViewSet(viewsets.ModelViewSet):
    # select_related because each CourseInstructor belongs to ONE course and ONE instructor
    queryset = CourseInstructor.objects.select_related(
        'course', 'instructor'
    ).all()
    serializer_class = CourseInstructorSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['qualification']
    filterset_fields = ['experience']
    ordering_fields = ['experience']
    ordering = ['-experience']


class MyEnrollmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
