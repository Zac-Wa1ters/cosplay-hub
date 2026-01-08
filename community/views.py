from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import *
from .models import *
from .permissions import *


def hub_home(request):
    return render(request, "community/hub_home.html")


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    follow_status = None

    if request.user.is_authenticated and request.user != user:
        follow = Follow.objects.filter(follower=request.user,following=user,).first()

        if follow:
            follow_status = follow.status
        else:
            follow_status = "not_following"

    if request.user == user or request.user.is_superuser:
        cosplays = user.cosplays.filter(archived=False)
    else:
        cosplays = user.cosplays.filter(archived=False,visibility="public")


    context = {
        "profile_user": user,
        "profile": profile,
        "cosplays": cosplays,
        "follow_status": follow_status,
    }

    return render(request, "community/profile_detail.html", context)



def cosplay_detail(request, cosplay_id):
    cosplay = get_object_or_404(Cosplay, id=cosplay_id)


    if cosplay.visibility == "private":
        if request.user != cosplay.owner and not request.user.is_superuser:
            return HttpResponseForbidden()


    elif cosplay.visibility == "followers":
        is_follower = Follow.objects.filter(follower=request.user,following=cosplay.owner,status="approved").exists()

    if (
        request.user != cosplay.owner
        and not is_follower
        and not request.user.is_superuser
    ):
        return HttpResponseForbidden()


    entries = cosplay.entries.prefetch_related("images").order_by("-created_at")

    return render(
        request,
        "community/cosplay_detail.html",
        {
            "cosplay": cosplay,
            "entries": entries,
        }
    )


@login_required
def profile_edit(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    permission = require_owner_or_admin(request, user)
    if permission:
        return permission

    profile = user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail",username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request,"community/profile_edit.html",{"form": form, "profile": profile,})

@login_required
def cosplay_create(request):
    if request.method == "POST":
        form = CosplayForm(request.POST)
        if form.is_valid():
            cosplay = form.save(commit=False)
            cosplay.owner = request.user
            cosplay.save()
            return redirect("profile_detail",username=request.user.username)
    else:
        form = CosplayForm()

    return render(
        request,"community/cosplay_form.html",{"form": form})

@login_required
def cosplay_delete(request, cosplay_id):
    cosplay = get_object_or_404(Cosplay, id=cosplay_id)

    permission = require_owner_or_admin(request, cosplay.owner)
    if permission:
        return permission

    if request.method == "POST":
        cosplay.delete()
        return redirect("profile_detail",username=cosplay.owner.username)

    return render(
        request,
        "community/cosplay_confirm_delete.html",
        {"cosplay": cosplay}
    )


@login_required
def cosplay_entry_create(request, cosplay_id):
    cosplay = get_object_or_404(Cosplay, id=cosplay_id)

    permission = require_owner_or_admin(request, cosplay.owner)
    if permission:
        return permission


    if request.method == "POST":
        entry_form = CosplayEntryForm(request.POST)
        images = request.FILES.getlist("images")

        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.cosplay = cosplay
            entry.save()

            for image in images:
                CosplayEntryImage.objects.create(entry=entry,image=image)

            return redirect("cosplay_detail",cosplay_id=cosplay.id)
    else:
        entry_form = CosplayEntryForm()

    return render(request,"community/entry_form.html",{"cosplay": cosplay,"form": entry_form,})

@login_required
def cosplay_entry_edit(request, entry_id):
    entry = get_object_or_404(CosplayEntry, id=entry_id)
    cosplay = entry.cosplay

    permission = require_owner_or_admin(request, cosplay.owner)
    if permission:
        return permission


    if request.method == "POST":
        form = CosplayEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("cosplay_detail", cosplay_id=cosplay.id)
    else:
        form = CosplayEntryForm(instance=entry)

    return render(
        request,
        "community/entry_edit.html",
        {
            "form": form,
            "cosplay": cosplay,
            "entry": entry,
        }
    )

@login_required
def cosplay_entry_delete(request, entry_id):
    entry = get_object_or_404(CosplayEntry, id=entry_id)
    cosplay = entry.cosplay

    permission = require_owner_or_admin(request, cosplay.owner)
    if permission:
        return permission

    if request.method == "POST":
        entry.delete()
        return redirect("cosplay_detail", cosplay_id=cosplay.id)

    return render(
        request,
        "community/entry_confirm_delete.html",
        {
            "entry": entry,
            "cosplay": cosplay,
        }
    )

@login_required
def follow_user(request, username):
    if request.method != "POST":
        return HttpResponseForbidden()

    target = get_object_or_404(User, username=username)

    if target == request.user:
        return redirect("profile_detail", username=username)

    profile = target.profile

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target,
    )

    if created:
        if profile.privacy == "public":
            follow.status = "approved"
        else:
            follow.status = "pending"
        follow.save()

    return redirect("profile_detail", username=username)




@login_required
def follow_requests(request):
    requests = Follow.objects.filter(
        following=request.user,
        status="pending"
    )

    return render(
        request,
        "community/follow_requests.html",
        {"requests": requests}
    )

@login_required
def approve_follow(request, follow_id):
    follow = get_object_or_404(Follow, id=follow_id, following=request.user)
    follow.status = "approved"
    follow.save()
    return redirect("follow_requests")


@login_required
def deny_follow(request, follow_id):
    follow = get_object_or_404(Follow, id=follow_id, following=request.user)
    follow.status = "denied"
    follow.save()
    return redirect("follow_requests")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(
                "profile_edit",
                username=user.username
            )
    else:
        form = UserCreationForm()

    return render(
        request,
        "community/signup.html",
        {"form": form}
    )

def events_list(request):
    events = Event.objects.filter(is_archived=False).order_by("start_time")
    return render(request, "community/events_list.html", {"events": events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_archived=False)
    return render(request, "community/event_detail.html", {"event": event})

@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect("event_detail", event_id=event.id)
    else:
        form = EventForm()

    return render(request, "community/event_form.html", {"form": form})

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    permission = require_owner_or_admin(request, event.creator)
    if permission:
        return permission

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_detail", event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, "community/event_form.html", {"form": form, "event": event})

@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    permission = require_owner_or_admin(request, event.creator)
    if permission:
        return permission

    if request.method == "POST":
        event.is_archived = True
        event.save()
        return redirect("events_list")

    return render(request, "community/event_confirm_delete.html", {"event": event})

@login_required
def event_post_create(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    permission = require_owner_or_admin(request, event.creator)
    if permission:
        return permission

    if request.method == "POST":
        form = EventPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.event = event
            post.author = request.user
            post.save()
            return redirect("event_detail", event_id=event.id)

    else:
        form = EventPostForm()

    return render(request, "community/event_post_form.html", {"form": form, "event": event})

@login_required
def event_comment_create(request, post_id):
    post = get_object_or_404(EventPost, id=post_id)

    if request.method == "POST":
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("event_detail", event_id=post.event.id)

    return HttpResponseForbidden()

@login_required
def event_post_delete(request, post_id):
    post = get_object_or_404(EventPost, id=post_id)
    permission = require_owner_or_admin(request, post.author)
    if permission:
        return permission

    if request.method == "POST":
        post.delete()
        return redirect("event_detail", event_id=post.event.id)

@login_required
def event_comment_delete(request, comment_id):
    comment = get_object_or_404(EventComment, id=comment_id)
    permission = require_owner_or_admin(request, comment.author)
    if permission:
        return permission

    if request.method == "POST":
        comment.delete()
        return redirect("event_detail", event_id=comment.post.event.id)
