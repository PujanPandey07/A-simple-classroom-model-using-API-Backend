from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import CourseInstructor


class IsAdminOrReadOnly(BasePermission):
    """
    Anyone can read (GET, HEAD, OPTIONS).
    Only admins can write (POST, PUT, PATCH, DELETE).
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsInstructorOfCourse(BasePermission):
    """
    Only the instructor assigned to this specific course
    can create/edit/delete its lessons.
    """

    def has_permission(self, request, view):
        # Always allow safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # For write actions, check if user is instructor of this course
        course_id = view.kwargs.get('course_pk')
        if not course_id:
            return False

        return CourseInstructor.objects.filter(
            course_id=course_id,
            instructor=request.user
        ).exists()


class IsStudentOwnerOrAdmin(BasePermission):
    """
    Students can only see their own enrollments.
    Admins can see all enrollments.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj here is an Enrollment instance
        return obj.student == request.user or request.user.is_staff
