from .models import Follow

def pending_follow_requests(request):
    if request.user.is_authenticated:
        count = Follow.objects.filter(
            following=request.user,
            status="pending"
        ).count()
    else:
        count = 0

    return {
        "pending_follow_requests": count
    }