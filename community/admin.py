from django.contrib import admin
from .models import Profile, Cosplay, CosplayEntry, CosplayEntryImage

admin.site.register(Profile)
admin.site.register(Cosplay)
admin.site.register(CosplayEntry)
admin.site.register(CosplayEntryImage)