from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, IncomingCorrespondence, Dispatch, Letters


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'department', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'department']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['email']

    # Fields shown when EDITING an existing user
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Fields shown when CREATING a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'department', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(IncomingCorrespondence)
admin.site.register(Dispatch)
admin.site.register(Letters)