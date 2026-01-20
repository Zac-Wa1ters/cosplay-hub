from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
        fields = ["image","title", "description", "location", "date", "time"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }


class EventPostForm(forms.ModelForm):
    class Meta:
        model = EventPost
        fields = ["content"]

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = EventComment
        fields = ["content"]

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 == password2:
            if password1.strip() == "":
                raise ValidationError(
                    "Password cannot be only whitespace."
                )

        return cleaned_data