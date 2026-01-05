from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


def hub_home(request):
    return render(request, "community/hub_home.html")


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    follow_status = None

    if request.user.is_authenticated and request.user != user:
        follow = Follow.objects.filter(
            follower=request.user,
            following=user,
        ).first()

        if follow:
            follow_status = follow.status
        else:
            follow_status = "not_following"

    if request.user == user:
        cosplays = user.cosplays.filter(archived=False)
    else:
        cosplays = user.cosplays.filter(
            archived=False,
            visibility="public"
        )

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
        if request.user != cosplay.owner:
            return HttpResponseForbidden()

    elif cosplay.visibility == "followers":
        is_follower = Follow.objects.filter(
            follower=request.user,
            following=cosplay.owner,
            status="approved"
        ).exists()

        if request.user != cosplay.owner and not is_follower:
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
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "community/profile_edit.html",
        {"form": form}
    )

@login_required
def cosplay_create(request):
    if request.method == "POST":
        form = CosplayForm(request.POST)
        if form.is_valid():
            cosplay = form.save(commit=False)
            cosplay.owner = request.user
            cosplay.save()
            return redirect(
                "profile_detail",
                username=request.user.username
            )
    else:
        form = CosplayForm()

    return render(
        request,
        "community/cosplay_form.html",
        {"form": form}
    )

@login_required
def cosplay_entry_create(request, cosplay_id):
    cosplay = get_object_or_404(Cosplay, id=cosplay_id)

    if cosplay.owner != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        entry_form = CosplayEntryForm(request.POST)
        images = request.FILES.getlist("images")

        if entry_form.is_valid():
            entry = entry_form.save(commit=False)
            entry.cosplay = cosplay
            entry.save()

            for image in images:
                CosplayEntryImage.objects.create(
                    entry=entry,
                    image=image
                )

            return redirect(
                "cosplay_detail",
                cosplay_id=cosplay.id
            )
    else:
        entry_form = CosplayEntryForm()

    return render(
        request,
        "community/entry_form.html",
        {
            "cosplay": cosplay,
            "form": entry_form,
        }
    )

@login_required
def cosplay_entry_edit(request, entry_id):
    entry = get_object_or_404(CosplayEntry, id=entry_id)
    cosplay = entry.cosplay

    if request.user != cosplay.owner:
        return HttpResponseForbidden()

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

    if request.user != cosplay.owner:
        return HttpResponseForbidden()

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
