from django.contrib import admin

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('phone_number', 'full_name', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('full_name', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('full_name', 'phone_number', 'password1', 'password2')}),
    )
    search_fields = ('full_name')
    ordering = ('phone_number',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

    admin.site.register(User, UserAdmin)
