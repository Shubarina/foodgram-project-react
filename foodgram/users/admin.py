from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_display_links = ('username',)
    search_fields = ('username',)
    list_filter = ('username', 'email')


admin.site.register(User, UserAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'reader')
    list_display_links = ('author',)
    list_filter = ('author', 'reader')


admin.site.register(Follow, FollowAdmin)
