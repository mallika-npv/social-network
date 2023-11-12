from django.contrib import admin
from .models import post, User, follow, like

# Register your models here.
admin.site.register(post)
admin.site.register(User)
admin.site.register(follow)
admin.site.register(like)