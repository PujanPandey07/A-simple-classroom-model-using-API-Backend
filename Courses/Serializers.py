from rest_framework import serializers
from .models import Course, Enrollment, CourseInstructor, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    # Field-level validation for title and price

    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError(
                "Title should be more than 5 characters.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "price should be a positive number")
        return value
    # Object_level validation for start_date and end_date

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError({
                    "end_date": "End date must be after start date."
                })

        return data  # always return the full data dict


class CourseInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInstructor
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
