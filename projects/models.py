from django.db import models
 
from django.contrib.auth.models import User



class Project(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    goal = models.IntegerField()

    image = models.URLField(blank=True, null=True)

    is_open = models.BooleanField(default=True)

    #date_created = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Pledge(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='pledges'
    )

    supporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pledges'
    )

    amount = models.IntegerField()

    anonymous = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pledge ${self.amount} to {self.project.title}"