# courses/models.py
from datetime import timezone
from django.db import models
from django.utils.text import slugify
from users.models import User

class Category(models.Model):
    """강의 분류 카테고리"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    STATUS_CHOICES = [
        ('draft', '초안'),
        ('published', '게시됨'),
        ('archived', '아카이브됨'),
    ]
    LEVEL_CHOICES = [
        ('beginner', '초급'),
        ('intermediate', '중급'),
        ('advanced', '고급'),
    ]

    # 기본 정보
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=150, blank=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    preview_video = models.URLField(blank=True)

    # 메타 정보
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'instructor'},
        related_name='courses_taught'
    )
    students = models.ManyToManyField(
        User, 
        through='Enrollment',
        related_name='courses_enrolled'
    )
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    language = models.CharField(max_length=50, default='한국어')
    difficulty = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # 수치 정보
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveIntegerField(default=0)
    total_duration = models.PositiveIntegerField(default=0)  # 총 강의 시간(분)
    max_students = models.PositiveIntegerField(default=0)  # 0 = 무제한

    # 시스템 필드
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['instructor']),
        ]
        ordering = ['-published_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def discounted_price(self):
        return self.price * (100 - self.discount) / 100

    def is_available(self):
        return self.status == 'published' and (
            self.max_students == 0 or 
            self.students.count() < self.max_students
        )

from django.db import models

class LessonResource(models.Model):
    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.CASCADE,
        related_name='lesson_resources'  # ✅ 고유한 related_name으로 변경
    )
    resource_file = models.FileField(upload_to='lesson_resources/')

class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    resources = models.ManyToManyField(
        LessonResource,
        related_name='related_lessons'  # ✅ 고유한 related_name으로 변경
    )


class Enrollment(models.Model):
    """수강 등록 정보"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [('student', 'course')]

    def save(self, *args, **kwargs):
        if self.completed and not self.completion_date:
            self.completion_date = timezone.now()
        super().save(*args, **kwargs)