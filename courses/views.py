from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course, Lesson, Enrollment
from .serializers import CourseSerializer, LessonSerializer
from common.permissions import IsInstructorOrAdmin
from rest_framework.views import APIView

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'instructor']:
            return Course.objects.all()
        return Course.objects.filter(enrollments__student=self.request.user)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsInstructorOrAdmin()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        course = self.get_object()
        course.is_published = True
        course.save()
        return Response({'status': 'course published'})

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsInstructorOrAdmin]
    
    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course_pk'])
    
    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        serializer.save(course=course)

class EnrollmentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        Enrollment.objects.create(course=course, student=request.user)
        return Response({'status': 'enrolled'}, status=status.HTTP_201_CREATED)
    
def index(request):
    # 예시 데이터 가져오기 (실제 데이터베이스 연결 필요)
    courses = Course.objects.all()[:5]  # 최신 5개의 강좌 목록

    return render(request, 'index.html', {
        'courses': courses,
    })