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

    PRIVACY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
    ]
    privacy = models.CharField(
        max_length=10,
        choices=PRIVACY_CHOICES,
        default="public",
    )


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



class Follow(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
    ]

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relationships",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relationships",
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} → {self.following} ({self.status})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="event_images/", blank=True, null=True)

    def __str__(self):
        return self.title


class EventPost(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class EventComment(models.Model):
    post = models.ForeignKey(EventPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
