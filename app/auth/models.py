import uuid
from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)  # Admin, Manager, Employee

    def __str__(self):
        return self.name
    
    
class User(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    
    def __str__(self):
        return self.email
    
    
class BlacklistedToken(models.Model):
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token