from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AssignmentViewSet, SubmissionViewSet

# Router 생성
router = DefaultRouter()

# 강좌별 과제 등록
router.register(r'courses/(?P<course_pk>\d+)/assignments', AssignmentViewSet, basename='assignment')

urlpatterns = [
    # AssignmentViewSet 엔드포인트 등록
    path('', include(router.urls)),

    # SubmissionViewSet 엔드포인트 등록 (과제별 제출물)
    path(
        'courses/<int:course_pk>/assignments/<int:assignment_pk>/submissions/',
        SubmissionViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='submission-list'
    ),
    path(
        'courses/<int:course_pk>/assignments/<int:assignment_pk>/submissions/<int:pk>/',
        SubmissionViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='submission-detail'
    ),
]
