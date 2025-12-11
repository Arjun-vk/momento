"""Instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('userregister',views.userregister,name='userregister'),
    path('userhome',views.userhome,name='userhome'),
    path('addpost',views.addpost,name='addpost'),
    path('mypost',views.mypost,name='mypost'),
    path('editpost/<int:id>',views.editpost,name='editpost'),
    path('deletepost/<int:id>',views.deletepost,name='deletepost'),
    path('addfriend',views.addfriend,name='addfriend'),
    path('follow/<int:id>',views.follow,name='follow'),
    path('frndrqst',views.frndrqst,name='frndrqst'),
    path('followback/<int:id>',views.followback,name='followback'),
    path('declinerqst/<int:id>',views.declinerqst,name='declinerqst'),
    path('myfriends',views.myfriends,name='myfriends'),
    path('myprofile',views.myprofile,name='myprofile'),
    path('like/<int:id>',views.like,name='like'),
    path('comment/<int:id>',views.comment,name='comment'),
    path('editmyprofile/<int:id>',views.editmyprofile,name='editmyprofile'),
    path('message/<int:id>/',views.message,name='message')

]
