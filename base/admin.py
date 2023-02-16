from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from base.models import Token, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "name", "date_joined", "is_email_verified", "is_staff", "is_superuser")
    readonly_fields = ("id", "date_joined", "last_login", "is_superuser", "is_staff")
    search_fields = ("email", "name")
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()
    ordering = ("email",)


class TokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at")


admin.site.register(Token, TokenAdmin)
