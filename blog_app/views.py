from django.shortcuts import render 
import datetime
from .models import Posts

# Create your views here.
def index(request):
    context = {
        'date': datetime.datetime.now(),
        'all_posts': Posts.objects.all()
    }
    return render(request, 'home.html', context)
