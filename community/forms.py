from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "display_name",
            "bio",
            "location",
            "privacy",
            "experience_level",
            "avatar",
        ]


class CosplayForm(forms.ModelForm):
    class Meta:
        model = Cosplay
        fields = [
            "title",
            "character_name",
            "franchise",
            "description",
            "status",
            "visibility",
        ]

class CosplayEntryForm(forms.ModelForm):
    class Meta:
        model = CosplayEntry
        fields = ["content"]

class CosplayEntryImageForm(forms.ModelForm):
    class Meta:
        model = CosplayEntryImage
        fields = ["image"]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["image","title", "description", "location", "start_time", "end_time"]

class EventPostForm(forms.ModelForm):
    class Meta:
        model = EventPost
        fields = ["content"]

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ["content"]
