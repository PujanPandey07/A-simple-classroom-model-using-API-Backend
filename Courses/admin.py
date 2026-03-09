from django.contrib import admin

# Register your models here.
from .models import Course, Enrollment, CourseInstructor, Lesson
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(CourseInstructor)
admin.site.register(Lesson)
