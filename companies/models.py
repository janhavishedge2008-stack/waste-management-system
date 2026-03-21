from django.db import models
from users.models import User


class WasteType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='♻️')  # emoji icon

    def __str__(self):
        return self.name


class CollectedWaste(models.Model):
    """Tracks inventory of waste collected from completed pickups."""
    waste_type = models.OneToOneField(WasteType, on_delete=models.CASCADE, related_name='inventory')
    total_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default='kg')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.waste_type.name}: {self.available_quantity} {self.unit} available"

    class Meta:
        verbose_name = 'Collected Waste Inventory'
        verbose_name_plural = 'Collected Waste Inventory'


class CompanyWasteRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    )

    company = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'company'})
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default='kg')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.username} - {self.waste_type.name} ({self.quantity}{self.unit})"

    class Meta:
        ordering = ['-created_at']
