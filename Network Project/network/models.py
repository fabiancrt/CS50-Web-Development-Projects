# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#here are the necessary models , here i also updated models to have the extra features i designed

#user has a new description field and also an is_banned status to check if the user is banned or not
class User(AbstractUser):
    is_banned = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

#only for moderation purposes
class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Moderate User'
        verbose_name_plural = 'Moderate Users'    
#post model that has the required fields and also an image field to upload images
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.content}"
    
    def likes_count(self):
        return self.likes.count()

#required like model
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user.username} likes {self.post.id}"

#also basic follow model
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

#profile model that has an extra profile picture field
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_profile_pic.jpg')

    def __str__(self):
        return f"{self.user.username}'s profile"

# necessary signals
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()