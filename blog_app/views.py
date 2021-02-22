from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
import datetime
from .models import User, Posts, Comments
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.

def allUsersPosts(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    user = User.objects.get(id=request.session['user_id'])
    user1 = User.objects.get(id=id)
    post1 = Posts.objects.filter(posted_by=user1)
    context={
        'user': user,
        'userPosts': user1,
        'posts' : post1.all().order_by('-created_at'),
        'all_users':User.objects.all()
    }
    return render(request, "usersallpost.html", context)

def create_comment(request, id):
    if 'user_id' not in request.session:
        return redirect('/login_page')
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        post = Posts.objects.get(id=id)
        Comments.objects.create(
            content = request.POST['content'],
            post = post,
            commented_by = user)
        return redirect(f'/details/{post.id}')
def details(request,id):
    post = Posts.objects.get(id=id)
    current_user = User.objects.get(id = request.session['user_id'])
    comments = post.comments.order_by('-created_at')
    context={
        'post' : post,
        'user':current_user,
        'comments':comments
    }
    return render(request,"post_details.html",context )

def like_Home(request, id):
    user = User.objects.get(id=request.session['user_id'])
    post = Posts.objects.get(id=id)
    liked = False
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return redirect(f'/home')

def likeDetails(request, id):
    user = User.objects.get(id=request.session['user_id'])
    post = Posts.objects.get(id=id)
    liked = False
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return redirect(f'/details/{post.id}')

def likeAllposts(request, id1, id2):
    user = User.objects.get(id=request.session['user_id'])
    post = Posts.objects.get(id = id1)
    user1 = User.objects.get(id = id2)
    liked = False
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return redirect(f'/allposts/{user1.id}')


def create_post(request):
    if request.method == "GET":
        return redirect('/home')
    errors = Posts.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/create')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Posts.objects.create(
            header_image = request.FILES['header_image'],
            title = request.POST['title'],
            content = request.POST['content'],
            posted_by = user,
        )
        return redirect('/home')

def create_page(request):
    return render (request,'create_post.html')

def home(request):
    if 'user_id' not in request.session:
        return redirect('/login_page')
    context={
        'user':User.objects.get(id = request.session['user_id']),
        'posts':Posts.objects.all().order_by('-created_at'),
        'all_users':User.objects.all()
    }
    return render(request,"home.html", context)


def logout(request):
    request.session.clear()
    return redirect('/')
def login(request):
    if request.method == "GET":
        return redirect('/login_page')
    if not User.objects.authenticate(request.POST['user_name'], request.POST['password']):
        messages.error(request, 'Invalid Username and Password')
        return redirect('/login_page')
    user = User.objects.get(user_name=request.POST['user_name'])
    request.session['user_id']=user.id
    return redirect('/home')
def login_page(request):
    return render(request, "login.html")

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/register')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/home')
def register_page(request):
    return render(request, "registerLogin.html")

def landing_page(request):
    return render(request, 'landing_page.html',{})













