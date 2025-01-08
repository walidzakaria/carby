from django.contrib import admin
from .models import UserProfile, UserView, ActiveUser

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', )
    search_fields = ('user__username', 'phone_number', )


class UserViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin', )
    search_fields = ('user__username', )
    
    list_filter = ('is_admin', )


class ActiveUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_seen', )
    search_fields = ('user__username', )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserView, UserViewAdmin)
admin.site.register(ActiveUser, ActiveUserAdmin)
