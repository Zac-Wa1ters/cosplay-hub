from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, CosplayForm, CosplayEntryForm
from .models import Cosplay, CosplayEntry, CosplayEntryImage


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

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
    }

    return render(request, "community/profile_detail.html", context)


def cosplay_detail(request, cosplay_id):
    cosplay = get_object_or_404(Cosplay, id=cosplay_id)


    if cosplay.visibility == "private":
        if request.user != cosplay.owner:
            return HttpResponseForbidden()

    if cosplay.visibility == "followers":
        if request.user != cosplay.owner:
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
