from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TodoItem(models.Model):
    content = models.TextField()
    archive = models.BooleanField(default=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    deleted = models.BooleanField(default=False)
