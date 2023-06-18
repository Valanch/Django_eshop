from django.contrib import admin

from accounts.models import Role, Profile


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "name", "role", "avatar", "email", "phone"
