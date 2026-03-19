from django.db import models
from django.conf import settings
# Create your models here.




User = settings.AUTH_USER_MODEL

class Ride(models.Model):

    class Status(models.TextChoices):
        REQUESTED = 'requested', 'Requested'
        ACCEPTED  = 'accepted', 'Accepted'
        STARTED   = 'started', 'Started'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='drives')

    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REQUESTED
    )
    current_location = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)

