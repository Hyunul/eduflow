from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from common.logger import log_event
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils.timezone import now
from common.logger import log_event

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    log_event(f'✅ 로그인 성공: {user.username} | IP: {ip} | {now()}')

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    ip = get_client_ip(request)
    log_event(f'❌ 로그인 실패: 사용자명={credentials.get("username")} | IP: {ip} | {now()}', level='warning')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    log_event(f'🚪 로그아웃: {user.username} | IP: {ip} | {now()}')

def get_client_ip(request):
    """사용자 IP 주소 가져오기"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(post_save, sender=User)
def user_activity_log(sender, instance, created, **kwargs):
    if created:
        log_event(f'👤 새로운 사용자 등록: {instance.username}')
    else:
        log_event(f'📝 사용자 정보 업데이트: {instance.username}')

@receiver(post_save, sender=User)
def password_change_log(sender, instance, **kwargs):
    if instance.has_usable_password():
        log_event(f'🔐 {instance.username} 사용자가 비밀번호를 변경했습니다.', level='warning')
