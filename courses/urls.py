from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, EnrollmentView

# Router 생성
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

# URL 패턴 정의
urlpatterns = [
    path('', include(router.urls)),
    path('courses/<int:course_pk>/lessons/', LessonViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='lesson-list'),
    path('courses/<int:course_pk>/lessons/<int:pk>/', LessonViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='lesson-detail'),
    path('courses/<int:course_id>/enroll/', EnrollmentView.as_view(), name='enroll-course'),
    path('courses/<int:pk>/publish/', CourseViewSet.as_view({'post': 'publish'}), name='course-publish'),
]
