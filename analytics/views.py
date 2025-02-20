from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.db.models import Count, Avg
from courses.models import Course, Enrollment
from users.models import User

class LearningAnalyticsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # AI 분석을 위한 기본 데이터
        data = {
            'total_students': User.objects.filter(role='student').count(),
            'active_courses': Course.objects.annotate(
                enroll_count=Count('enrollments')
                .filter(enroll_count__gt=0).count())
        }
        return Response(data)

class CourseStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        stats = {
            'enrollments': course.enrollments.count(),
            'avg_submissions': Assignment.objects.filter(course=course)
                .annotate(sub_count=Count('submissions'))
                .aggregate(avg=Avg('sub_count'))['avg']
        }
        return Response(stats)