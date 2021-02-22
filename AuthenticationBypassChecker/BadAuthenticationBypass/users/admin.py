from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    forms = UserChangeForm
    add_form = UserCreationForm

    list_display = ('get_full_name', 'email', 'nickname', 'is_active', 'is_superuser', 'date_joined')
    list_filter = ('is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('nickname', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'nickname')
    ordering = ('-date_joined',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)