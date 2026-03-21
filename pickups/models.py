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

    WASTE_CATEGORY_CHOICES = (
        ('recyclable', 'Recyclable'),
        ('non_recyclable', 'Non-Recyclable'),
        ('hazardous', 'Hazardous'),
        ('organic', 'Organic'),
        ('electronic', 'Electronic (E-Waste)'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickups')
    waste_type = models.ForeignKey(WasteType, on_delete=models.CASCADE)
    waste_category = models.CharField(max_length=20, choices=WASTE_CATEGORY_CHOICES, blank=True)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_date = models.DateField()
    pickup_time = models.TimeField(null=True, blank=True)
    quantity_estimate = models.CharField(max_length=50, blank=True)
    special_instructions = models.TextField(blank=True)
    waste_image = models.ImageField(upload_to='pickups/images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Assignment
    assigned_company = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_pickups', limit_choices_to={'user_type': 'company'}
    )
    assigned_worker = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='worker_pickups', limit_choices_to={'user_type': 'worker'}
    )
    admin_notes = models.TextField(blank=True)

    # QR code
    qr_code = models.ImageField(upload_to='pickups/qr/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.waste_type.name} - {self.pickup_date}"

    def generate_qr(self):
        """Generate QR code image for this pickup."""
        try:
            import qrcode
            from io import BytesIO
            from django.core.files import File
            data = f"EcoWaste Pickup #{self.pk} | User: {self.user.username} | Waste: {self.waste_type.name} | Date: {self.pickup_date} | Status: {self.status}"
            qr = qrcode.make(data)
            buf = BytesIO()
            qr.save(buf, format='PNG')
            buf.seek(0)
            self.qr_code.save(f'qr_{self.pk}.png', File(buf), save=False)
        except Exception:
            pass

    class Meta:
        ordering = ['-created_at']
