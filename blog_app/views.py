from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from .models import User, Posts, Comments

# Create your views here.
def register_page(request):
    return render(request, "registerLogin.html")
def login_page(request):
    return render(request, "login.html")

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You successfully registered!")
        return redirect('/success')

def index(request):
    context = {
        'date': datetime.datetime.now(),
        'all_posts': Posts.objects.all()
    }
    return render(request, 'landing_page.html', context)