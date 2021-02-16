from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class Log_Reg_Manager(models.Manager):
    
    def validate(self, form):
        errors = {}
        # add keys and values to errors dictionary for each invalid fieldcopy
        if len(form['user_name']) < 2:
            errors["first_name"] = "Username should be at least 2 characters"
        if len(form['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(form['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Address'
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already taken"
        if len(form['password'])<8:
            errors['password'] = 'Password must be at least 8 characters'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors

    def authenticate(self,email,password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(),user.password.encode())
    
    def register(self,form):
        pw=bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name=form['first_name'],
            last_name=form['last_name'],
            email = form['email'],
            password= pw,
        )

class User(models.Model):
    user_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    objects = Log_Reg_Manager()

class Posts(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comments(models.Model):
    name = models.CharField(max_length = 100)
    content = models.TextField()
    post = models.ForeignKey(Posts, related_name="comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)