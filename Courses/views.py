from rest_framework import viewsets, permissions
from .models import Course, Enrollment, CourseInstructor, Lesson
from .Serializers import CourseSerializer, EnrollmentSerializer, CourseInstructorSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # later you can make instructor permission
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CourseInstructorViewSet(viewsets.ModelViewSet):
    queryset = CourseInstructor.objects.all()
    serializer_class = CourseInstructorSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # later you can make instructor permission
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Enrollment.objects.filter(course_id=course_id)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # later you can make student permission
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class LessonViewSet(viewsets.ModelViewSet):

    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Lesson.objects.filter(course_id=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs['course_pk']
        serializer.save(course_id=course_id)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # later you can make instructor permission
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
