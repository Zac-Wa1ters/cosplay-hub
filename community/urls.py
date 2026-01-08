from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", hub_home, name="hub_home"),
    path("signup/", signup, name="signup"),
    path("users/<str:username>/", profile_detail, name="profile_detail"),
    path("cosplay/<int:cosplay_id>/", cosplay_detail, name="cosplay_detail"),
    path("profile/edit/<str:username>/", profile_edit, name="profile_edit"),
    path("cosplay/create/", cosplay_create, name="cosplay_create"),
    path("cosplay/<int:cosplay_id>/entry/create/", cosplay_entry_create, name="cosplay_entry_create"),
    path("entry/<int:entry_id>/edit/",cosplay_entry_edit,name="cosplay_entry_edit"),
    path("entry/<int:entry_id>/delete/",cosplay_entry_delete,name="cosplay_entry_delete"),
    path("login/",auth_views.LoginView.as_view(template_name="community/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("users/<str:username>/follow/",follow_user,name="follow_user"),
    path("follow/requests/", follow_requests, name="follow_requests"),
    path("follow/<int:follow_id>/approve/", approve_follow, name="approve_follow"),
    path("follow/<int:follow_id>/deny/", deny_follow, name="deny_follow"),
    path("cosplay/<int:cosplay_id>/delete/", cosplay_delete, name="cosplay_delete"),
    path("events/", events_list, name="events_list"),
    path("events/create/", event_create, name="event_create"),
    path("events/<int:event_id>/", event_detail, name="event_detail"),
    path("events/<int:event_id>/edit/", event_edit, name="event_edit"),
    path("events/<int:event_id>/delete/", event_delete, name="event_delete"),
    path("events/<int:event_id>/posts/create/", event_post_create, name="event_post_create"),
    path("events/posts/<int:post_id>/comment/", event_comment_create, name="event_comment_create"),
    path("events/posts/<int:post_id>/delete/", event_post_delete, name="event_post_delete"),
    path("events/comments/<int:comment_id>/delete/", event_comment_delete, name="event_comment_delete"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
