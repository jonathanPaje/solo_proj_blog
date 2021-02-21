from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path('register', views.register_page),
    path('login_page', views.login_page),
    path('submit-reg', views.register),
    path('login', views.login),
    path('logout',views.logout),
    path('home',views.home),
    path('create',views.create_page),
    path('create-post', views.create_post),
    path('likeOnHome/<int:id>', views.like_Home),
    path('likeOnDetails/<int:id>',views.likeDetails),
    path('details/<int:id>', views.details),
    path('create_comment/<int:id>',views.create_comment),
]