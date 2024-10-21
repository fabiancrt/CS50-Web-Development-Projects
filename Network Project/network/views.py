from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, Post, Like, Follow
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import ProfilePictureForm
from .models import Profile
from django.contrib import messages

#hello there CS50 team , my name is Fabian Cretu and this is my version of the network project that the team requested. 
#this project satisfies the specifications on the website but i also decided to add some extra features to make it my own , everthin i have done will be explained
#in the video and also to help you guys understand what i have done better i will add comments throughout the code to explain what i have done


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            if user.is_banned:
                return render(request, "network/login.html", {
                    "message": "You are banned from the website."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

#here is the required index where both logged in user and users that are not logged in can see all the posts(i also included image display inside the posts and 
# mini pictograms)
def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {'page_obj': page_obj})

#the post creation view that was requrired , it satisfied the specifications so that the user can create a simple post but i added the ability
#  to add an image to the post
@login_required(login_url='/login')
@csrf_exempt
def post_creation(request):
    if request.method == "POST":
        content = request.POST["content"]
        image = request.FILES.get('image')  # the image i was talking about
        post = Post(user=request.user, content=content, image=image)
        post.save()
        return redirect('index')
    return render(request, "network/new_post.html")

#the profile view that was also required by the team , but here i added many extra features , the ability to add profile pictures , descriptions & admin status
@login_required(login_url='/login')
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        posts = user.posts.all().order_by('-timestamp')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        is_following = request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=user).exists()
        
        # followers as specified
        followers_count = Follow.objects.filter(following=user).count()
        following_count = Follow.objects.filter(follower=user).count()
        
        return render(request, "network/profile.html", {
            'profile_user': user,
            'page_obj': page_obj,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
        })
    except User.DoesNotExist:
        return render(request, 'network/no_user_found.html', {'username': username})

#the view that grants user the ability to follow others(also required)
@login_required(login_url='/login')
def follow(request, username):
    user = get_object_or_404(User, username=username)
    if Follow.objects.filter(follower=request.user, following=user).exists():
        Follow.objects.filter(follower=request.user, following=user).delete()
    else:
        Follow.objects.create(follower=request.user, following=user)
    return redirect('profile', username=username)

#the view required for the like_post function to work , same as the required one but i added visual changes mostly (an actual heart button for likes)
@login_required(login_url='/login')
@csrf_exempt
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True
        return JsonResponse({
            'success': True,
            'likes_count': post.likes_count(),
            'is_liked': is_liked
        })

    elif request.method == 'GET':
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
        return JsonResponse({'is_liked': is_liked})

    return JsonResponse({'error': 'Invalid request'}, status=400)

#the view that displays all the posts of the users that the user is following(this was also required)
@login_required(login_url='/login')
def following(request):
    following_users = request.user.following.all().values_list('following', flat=True)
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {'page_obj': page_obj})

#the edit post feature (also has little visual changes)
@login_required(login_url='/login')
@csrf_exempt
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == "PUT":
        data = json.loads(request.body)
        post.content = data.get("content", "")
        post.save()
        return JsonResponse({'content': post.content, 'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

#this feature i added myself, the ability to remove a post , works through the delete method
@login_required(login_url='/login')
@csrf_exempt
def remove_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == "DELETE":
        post.delete()
        return JsonResponse({'content': post.content, 'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


#also extra feature i implemented , the ability to change user profile picture that gets displayed across the whole site
@login_required(login_url='/login')
@csrf_exempt
def change_profile_picture(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfilePictureForm(instance=profile)
    return render(request, 'network/change_profile_picture.html', {'form': form})

#& finally the last extra feature i added , custom descriptions for users
@login_required(login_url='/login')
def edit_description(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        request.user.description = description
        request.user.save()
        messages.success(request, 'Description updated successfully.')
        return redirect('profile', username=request.user.username)
    return redirect('profile', username=request.user.username)