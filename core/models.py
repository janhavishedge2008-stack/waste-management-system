from django.db import models
from django.utils import timezone
import random

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class WasteTip(models.Model):
    tip = models.TextField()
    category = models.CharField(max_length=50, default='general')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.tip[:60]

    @classmethod
    def get_tip_of_the_day(cls):
        tips = list(cls.objects.filter(active=True))
        if not tips:
            return None
        # Use day-of-year as seed so it changes daily but is consistent within a day
        random.seed(timezone.now().timetuple().tm_yday)
        return random.choice(tips)
