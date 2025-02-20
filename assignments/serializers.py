from rest_framework import serializers
from .models import Assignment, Submission
from courses.models import Course
from users.models import User

class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('submitted_at',)