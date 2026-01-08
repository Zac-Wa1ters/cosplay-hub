from django.http import HttpResponseForbidden

def require_owner_or_admin(request, owner):
    if not (request.user.is_superuser or request.user == owner):
        return HttpResponseForbidden()
    return None
