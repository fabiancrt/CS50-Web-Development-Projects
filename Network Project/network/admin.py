# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProxy, Post, Like, Follow, Profile

#custom admin.py for the admin user to have an easier time moderating the website ( also has the ability to ban or unban users)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_banned')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_banned')
    inlines = (ProfileInline,)
    actions = ['ban_user', 'unban_user']

    def ban_user(self, request, queryset):
        queryset.update(is_banned=True)
    ban_user.short_description = 'Ban selected users'

    def unban_user(self, request, queryset):
        queryset.update(is_banned=False)
    unban_user.short_description = 'Unban selected users'

class ModerateUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_banned')
    search_fields = ('username', 'email')
    list_filter = ('is_banned',)
    actions = ['ban_user', 'unban_user']

    def ban_user(self, request, queryset):
        queryset.update(is_banned=True)
    ban_user.short_description = 'Ban selected users'

    def unban_user(self, request, queryset):
        queryset.update(is_banned=False)
    unban_user.short_description = 'Unban selected users'

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp', 'likes_count')
    search_fields = ('user__username', 'content')
    list_filter = ('timestamp',)
    readonly_fields = ('likes_count',)
    actions = ['remove_post']

    def remove_post(self, request, queryset):
        queryset.delete()
    remove_post.short_description = 'Remove selected posts'

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__content')

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    search_fields = ('follower__username', 'following__username')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'get_description')
    search_fields = ('user__username',)

    def get_description(self, obj):
        return obj.user.description
    get_description.short_description = 'Description'

admin.site.register(User, UserAdmin)
admin.site.register(UserProxy, ModerateUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Profile, ProfileAdmin)