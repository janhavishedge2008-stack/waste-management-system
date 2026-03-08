from django.db import models
from users.models import User
from companies.models import WasteType

class PickupRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    pickup_date = models.DateField()
    pickup_time = models.TimeField(null=True, blank=True)
    quantity_estimate = models.CharField(max_length=50, blank=True)
    special_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.waste_type.name} - {self.pickup_date}"
    
    class Meta:
        ordering = ['-created_at']
