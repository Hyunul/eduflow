from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Assignment, Submission
from courses.models import Course
from .serializers import AssignmentSerializer, SubmissionSerializer
from common.permissions import IsInstructorOrAdmin, IsSubmissionOwner

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsInstructorOrAdmin]
    
    def get_queryset(self):
        return Assignment.objects.filter(course_id=self.kwargs['course_pk'])
    
    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        serializer.save(course=course)

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, IsSubmissionOwner]
    
    def get_queryset(self):
        return Submission.objects.filter(
            assignment_id=self.kwargs['assignment_pk'],
            student=self.request.user
        )
    
    def perform_create(self, serializer):
        assignment = Assignment.objects.get(pk=self.kwargs['assignment_pk'])
        serializer.save(student=self.request.user, assignment=assignment)