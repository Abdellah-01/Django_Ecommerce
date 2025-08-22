from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'date_joined', 'last_logined',
        'is_admin', 'is_staff', 'is_active', 'is_superadmin'
    )
    list_display_links = ('email', 'first_name', 'last_name')  # ✅ fixed
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_logined')  # ✅ matches your model
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
