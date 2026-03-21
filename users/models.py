from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('company', 'Company'),
        ('worker', 'Worker/Collector'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='regular')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    reward_points = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    avatar_color = models.CharField(max_length=7, default='#28a745')
    created_at = models.DateTimeField(auto_now_add=True)

    # Email verification
    is_email_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    def get_level(self):
        if self.reward_points >= 500:
            return ('Platinum', '🏆')
        elif self.reward_points >= 200:
            return ('Gold', '🥇')
        elif self.reward_points >= 100:
            return ('Silver', '🥈')
        else:
            return ('Bronze', '🥉')

    def generate_otp(self):
        from django.utils import timezone
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.save(update_fields=['otp_code', 'otp_created_at'])
        return self.otp_code

    def is_otp_valid(self, code):
        from django.utils import timezone
        import datetime
        if not self.otp_code or not self.otp_created_at:
            return False
        if self.otp_code != code:
            return False
        expiry = self.otp_created_at + datetime.timedelta(minutes=10)
        return timezone.now() <= expiry


class Notification(models.Model):
    NOTIF_TYPES = (
        ('pickup', 'Pickup Update'),
        ('reward', 'Reward Points'),
        ('system', 'System'),
        ('company', 'Company'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"


# Proxy models for admin separation
class RegularUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Regular User'
        verbose_name_plural = 'Regular Users'


class CompanyUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Company User'
        verbose_name_plural = 'Company Users'


class WorkerUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Worker/Collector'
        verbose_name_plural = 'Workers/Collectors'
