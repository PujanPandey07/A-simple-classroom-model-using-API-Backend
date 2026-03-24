from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import CourseInstructorViewSet, CourseViewSet, EnrollmentViewSet, LessonViewSet, MyEnrollmentsView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'course-instructors', CourseInstructorViewSet)
urlpatterns = router.urls+[
    path('courses/<int:course_pk>/enrollments/',
         EnrollmentViewSet.as_view({'get': 'list', 'post': 'create'}), name='enrollment-list'),
    path('courses/<int:course_pk>/enrollments/<int:pk>/',
         EnrollmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='enrollment-detail'),
    path('courses/<int:course_pk>/lessons/',
         LessonViewSet.as_view({'get': 'list', 'post': 'create'}), name='lesson-list'),
    path('courses/<int:course_pk>/lessons/<int:pk>/',
         LessonViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='lesson-detail'),
    path('my-enrollments/',
         MyEnrollmentsView.as_view(), name='my-enrollments'),
]
