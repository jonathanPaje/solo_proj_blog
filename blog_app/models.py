from django.db import models
# from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class Log_Reg_Manager(models.Manager):
    def validate(self, form):
        errors = {}
        # add keys and values to errors dictionary for each invalid fieldcopy
        if len(form['user_name']) < 2:
            errors['user_name'] = "Username should be at least 2 characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already taken"
        if len(form['password']) < 7:
            errors['password'] = 'Password must be at least 8 characters'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors

    def authenticate(self,username,password):
        users = self.filter(user_name = username)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(),user.password.encode())
    
    def register(self,form):
        pw=bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            user_name=form['user_name'],
            email = form['email'],
            password= pw,
        )

class User(models.Model):
    user_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    objects = Log_Reg_Manager()


class PostManager(models.Manager):
    
    def validate(self, form):
        errors = {}
        if len(form['title']) < 1:
            errors["quoter"] = "Don't forget a title"
        if len(form['content']) < 1:
            errors["quote"] = "Add content to your post"
        
        return errors

class Posts(models.Model):
    header_image = models.ImageField(null=True, blank =True, upload_to="images/")
    title = models.CharField(max_length = 100)
    content = RichTextField(blank=True, null=True)
    # content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name='user_post',  on_delete = models.CASCADE)
    objects = PostManager()
    likes = models.ManyToManyField(User, related_name="liked_posts")

    def __repr__(self):
        return self.title + '|' + str(self.posted_by)


class Comments(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Posts, related_name="comments", on_delete = models.CASCADE)
    commented_by = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment object: from:{self.commented_by} on {self.post} post"