from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html

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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "thumbnail", "city", "state", "country", "pincode")  # added pincode
    search_fields = ("user__email", "user__first_name", "user__last_name", "city", "state", "country", "pincode")
    list_filter = ("country", "state", "city")

    readonly_fields = ("thumbnail",)  # show preview in detail page

    fieldsets = (
        ("User Info", {
            "fields": ("user", "thumbnail", "profile_picture")
        }),
        ("Address", {
            "fields": ("address_line_1", "address_line_2", "city", "state", "country", "pincode")  # added here
        }),
    )

    def thumbnail(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%; object-fit:cover;" />',
                obj.profile_picture.url
            )
        return "No Image"
    thumbnail.short_description = "Profile Picture"
