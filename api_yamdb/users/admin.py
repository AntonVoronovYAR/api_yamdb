from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ('is_superuser', 'username', 'email', 'bio', 'role',
              'is_active', 'is_staff',)
    list_display = ('username', 'role', 'is_superuser', 'is_admin')


admin.site.register(User, UserAdmin)
