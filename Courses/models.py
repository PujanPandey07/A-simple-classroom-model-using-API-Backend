from django.db import models
import uuid
from accounts.models import CustomUser


class Course(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class CourseInstructor(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='instructors')
    instructor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='teaching_courses')
    qualification = models.CharField(max_length=255)
    experience = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'instructor'],
                name='unique_course_instructor'
            )
        ]


class Enrollment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='enrolled_courses')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'student'],
                name='unique_course_student'
            )
        ]


class Lesson(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
