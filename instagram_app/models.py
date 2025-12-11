from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    user_type=models.CharField(max_length=100)

class User(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    mobile=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='profile_pic', blank=True,null=True)
    
class Post(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='Post')
    description=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now=True)

class Friends(models.Model):
    SENDER=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    RECEIVER=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    status=models.CharField(max_length=100)
    date_time=models.DateTimeField(auto_now=True)
    
class Message(models.Model):
    SENDER=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender1')
    RECEIVER=models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver1')
    chat=models.CharField(max_length=1000)
    date_time=models.DateTimeField(auto_now=True)

class Like(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    POST=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')

class Comment(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment')
    POST=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment')
    Comment=models.CharField(max_length=500)
    date_time=models.DateTimeField(auto_now=True)

