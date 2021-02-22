from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name = 'landing page'),
    path('about', views.about, name='about page from landing'),
    path('register', views.register_page, name='register page'),
    path('login_page', views.login_page, name='login page'),
    path('submit-reg', views.register, name='register user'),
    path('login', views.login, name='login user'),
    path('logout',views.logout, name= 'logout user'),
    path('home',views.home, name='homepage'),
    path('create',views.create_page, name='create post page'),
    path('create-post', views.create_post, name='create new post'),
    path('likeOnHome/<int:id>', views.like_Home, name='like on home page'),
    path('likeOnDetails/<int:id>',views.likeDetails, name= 'like on details page'),
    path('likeOnAllposts/<int:id1>/<int:id2>',views.likeAllposts, name= 'like on AllPost page'),
    path('details/<int:id>', views.details, name='details page of a post'),
    path('create_comment/<int:id>',views.create_comment, name='create comment'),
    path('allposts/<int:id>', views.allUsersPosts, name= "all of a user's posts"),
    path('edit-post/<int:id>', views.EditPost, name="edit post from modal"),
    path('delete-post/<int:id>', views.Delete, name="delete post from modal")
]