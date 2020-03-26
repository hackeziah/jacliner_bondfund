from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, MyAccountManager, UserInfo, Position, Company


class AccountAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'date_joined',
                    'last_login', 'is_admin', 'is_staff', 'is_user')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(UserAccount, AccountAdmin)
admin.site.register(UserInfo)
admin.site.register(Position)
admin.site.register(Company)
