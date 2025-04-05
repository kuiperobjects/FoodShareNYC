from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Measurement, Post


admin.site.register(Measurement)
admin.site.register(Post)
