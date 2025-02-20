from rest_framework import serializers
from .models import Course, Lesson
from users.models import User

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='instructor')
    )

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('course',)