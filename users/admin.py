from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_client', 'is_seller')
    list_filter = ('is_client', 'is_seller')
    search_fields = ('username', 'email')
    ordering = ('username',)
