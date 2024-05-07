from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from account.models import User

class UserModelAdmin(BaseUserAdmin):
    """
    Admin class for the User model.

    This class customizes the User model admin interface.
    """
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "email", "name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = (
        (None, {
            "classes": ["wide"],
            "fields": ("email", "name", "password1", "password2"),
        }),
    )
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

# Register your models here.
admin.site.register(User, UserModelAdmin)
