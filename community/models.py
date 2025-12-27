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
