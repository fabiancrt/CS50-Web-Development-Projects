
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

#specific urls , nothing special.

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.post_creation, name="new_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/<str:username>", views.follow, name="follow"),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path("following", views.following, name="following"),
    path('edit_post/<int:post_id>', views.edit_post, name='edit_post'),
    path('remove_post/<int:post_id>', views.remove_post, name='remove_post'),
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture'),
    path('edit_description/', views.edit_description, name='edit_description'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)