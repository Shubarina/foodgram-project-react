from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'recipes_count', 'followers_count')
    list_display_links = ('username',)
    search_fields = ('username',)
    list_filter = ('username', 'email')

    @admin.display(description='Количество рецептов')
    def recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Количество подписчиков')
    def followers_count(self, obj):
        return obj.following.count()


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'reader')
    list_display_links = ('author',)
    list_filter = ('author', 'reader')


admin.site.register(User, UserAdmin)

admin.site.register(Follow, FollowAdmin)
