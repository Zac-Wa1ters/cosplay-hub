from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    bio = models.TextField(blank = True)
    location = models.CharField(max_length=100, blank = True)
    EXPERIENCE_LEVELS = [
        ("casual", "Casual (Non-Competitive / Just for Fun)"),
        ("showcase", "Showcase (Exhibitions, Photoshoots, No Judging)"),
        ("novice", "Novice (0–1 Competitive Awards)"),
        ("journeyman", "Journeyman (2–3 Competitive Awards)"),
        ("master", "Master (4+ Awards / Professional / International)"),
    ]

    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVELS, default="casual")
    avatar = models.ImageField(upload_to="avatars/", blank = True, null = True)

    def __str__(self):
        return self.display_name

class Cosplay(models.Model):

    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("followers", "Followers Only"),
        ("private", "Private"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cosplays"
    )

    title = models.CharField(max_length=150)
    character_name = models.CharField(max_length=150)
    franchise = models.CharField(max_length=150, blank=True)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning"
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

class CosplayEntry(models.Model):


    cosplay = models.ForeignKey(
        Cosplay,
        on_delete=models.CASCADE,
        related_name="entries"
    )

    content = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entry for {self.cosplay.title}"

class CosplayEntryImage(models.Model):

    entry = models.ForeignKey(
        CosplayEntry,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="cosplay_entries/")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for entry {self.entry.id}"
