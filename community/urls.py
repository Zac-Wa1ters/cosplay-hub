from django.urls import path
from .views import (profile_detail, cosplay_detail, profile_edit, cosplay_create, cosplay_entry_create, cosplay_entry_edit, cosplay_entry_delete)

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("users/<str:username>/", profile_detail, name="profile_detail"),
    path("cosplay/<int:cosplay_id>/", cosplay_detail, name="cosplay_detail"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("cosplay/create/", cosplay_create, name="cosplay_create"),
    path("cosplay/<int:cosplay_id>/entry/create/", cosplay_entry_create, name="cosplay_entry_create"),
    path("entry/<int:entry_id>/edit/",cosplay_entry_edit,name="cosplay_entry_edit"),
    path("entry/<int:entry_id>/delete/",cosplay_entry_delete,name="cosplay_entry_delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
