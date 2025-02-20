from django.db import models
from users.models import User
from courses.models import Course
from assignments.models import Assignment

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField()
    graded_at = models.DateTimeField(auto_now_add=True)