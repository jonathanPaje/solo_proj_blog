from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from .models import User, Posts, Comments

# Create your views here.
def landing_page(request):
    return render(request, 'landing_page.html')
def register_page(request):
    return render(request, "registerLogin.html")
def login_page(request):
    return render(request, "login.html")
def home(request):
    return render(request,"home.html")

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

def login(request):
    if request.method == "GET":
        return redirect('/login_page')
    if not User.objects.authenticate(request.POST['user_name'], request.POST['password']):
        messages.error(request, 'Invalid Username and Password')
        return redirect('/login_page')
    user = User.objects.get(user_name=request.POST['user_name'])
    request.session['user_id']=user.id
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')