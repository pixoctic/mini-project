from django.db import models
from django.contrib.auth.models import User
import uuid

class ServiceRequest(models.Model):
    # Defining the stages of the repair
    STATUS_CHOICES = [
        ('Pending', 'Pending Drop-off'),
        ('Diagnosing', 'Diagnosing Issue'),
        ('Repairing', 'In Repair'),
        ('Completed', 'Ready for Pickup'),
    ]

    # Linking the request to the logged-in customer
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    device_brand = models.CharField(max_length=50)
    device_model = models.CharField(max_length=50)
    imei_number = models.CharField(max_length=20)
    issue_description = models.TextField()
    
    # Tracking and admin fields
    tracking_id = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            # Auto-generates a unique 8-character ID (e.g., 4A9F2B1C)
            self.tracking_id = str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device_brand} {self.device_model} - {self.tracking_id}"
