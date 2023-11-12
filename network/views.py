from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, post, follow, like
import json

def index(request):
    allposts = post.objects.all().order_by("timestamp").reverse()
    alllikes = like.objects.all()
    liked = []
    likes = {}
    for i in allposts:
        likes[i.pk] = 0
        
    for i in alllikes:
        if i.lpost.pk in likes:
            likes[i.lpost.pk] += 1
        else:
            likes[i.lpost.pk] = 1
        if i.user == request.user:
            liked.append(i.lpost)
    paginator = Paginator(allposts, 2)
    pno = request.GET.get('page')
    posts = paginator.get_page(pno)
    return render(request, "network/index.html",{
        "posts" : posts,
        "liked" : liked,
        "likes" : likes,
    })

def alike(request, id):
    lpost = post.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    new = like(user=user, lpost=lpost)
    new.save()
    return redirect('index')

def rlike(request, id):
    lpost = post.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    p = like.objects.filter(user=user,lpost=lpost)
    p.delete()
    return redirect('index')

def newpost(request):
    if request.method == 'POST':
        content = request.POST['newpost']
        user = User.objects.get(pk=request.user.id)
        new = post(content=content, author=user)
        new.save()
        return HttpResponseRedirect(reverse(index))
    
def edit(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        edit_post = post.objects.get(pk=id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "change succesful", "data":data["content"]})

def profile(request, id):
    c_user = User.objects.get(pk=id)
    isuser = request.user == c_user
    if_following = follow.objects.filter(user=request.user, following=c_user) 
    following = follow.objects.filter(user=c_user).count()
    follower =  follow.objects.filter(following=c_user).count()
    posts = post.objects.filter(author = id).order_by("timestamp").reverse()
    return render(request, "network/profile.html",{
        "posts" : posts,
        "c_user" : c_user,
        "isuser" : isuser,
        "following" : following,
        "follower" : follower,
        "if_following" : if_following
    })
    
def count(request, id):
    user = request.user
    following = User.objects.get(pk=id)
    new = follow(user=user, following = following)
    new.save()
    return redirect('profile', id=id)

def uncount(request, id):
    user = request.user
    following = User.objects.get(pk=id)
    old = follow.objects.get(user=user, following=following)
    old.delete()
    return redirect('profile', id=id)

def f_page(request):
    user = request.user
    people = follow.objects.filter(user=user)
    allposts=[]
    for person in people:
        p = post.objects.get(author=person.following)
        allposts.append(p)

    paginator = Paginator(allposts, 10)
    pno = request.GET.get('page')
    posts = paginator.get_page(pno)
    return render(request, "network/following.html",{
        "posts" : posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
