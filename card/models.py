import uuid
from django.db import models
from users.models import User

class Card(models.Model):
    status_choices = (
        ('Active', 'Active'),
        ('Disable', 'Disable'),
        ('Pending', 'Pending')
    )
    card_number = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, models.CASCADE, related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    card_status = models.CharField(max_length=15, choices=status_choices)

def __str__(self):
    return self.title


