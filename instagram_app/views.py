from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from . models import *
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        query1=Login.objects.filter(username=username,password=password).exists()
        if query1:
            query2=Login.objects.get(username=username,password=password)
            request.session["lid"]=query2.pk
            lid=request.session.get('lid')
            if query2.user_type=='user':
                u=User.objects.get(LOGIN=lid)
                request.session["user_id"]=u.pk
                return redirect('/userhome')
        else:
            return HttpResponse(f"<script>alert('Username or password incorrect...!');window.location='/login'</script>")

    return render(request,'login.html')

def userregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST['mobile']
        email = request.POST['email']
        photo=request.FILES.get('photo')
        username = request.POST['username']
        password = request.POST['password']

        # Create login table entry
        login_obj = Login.objects.create(
            username=username,
            password=password,
            user_type='user'
        )

        print(photo,'ppphhh')

        if photo:

            q1=User.objects.create(
                LOGIN=login_obj,
                name=name,
                mobile=mobile,
                email=email,
                photo=photo

            )
            q1.save()
            print("save with photo")

        else:
            q2=User.objects.create(
                LOGIN=login_obj,
                name=name,
                mobile=mobile,
                email=email
                

            )
            q2.save()
            print("save without photo")


        return HttpResponse("<script>alert('Registration Successful!');window.location='/login'</script>")

    return render(request, 'register.html')

def userhome(request):
    q1=Post.objects.all().order_by('-date_time')
    return render(request,'userhome.html',{'data':q1})

def addpost(request):
    if request.method=='POST':
        Image=request.FILES.get('image')
        Desc=request.POST['description']
        q1=Post.objects.create(image=Image,description=Desc,USER_id=request.session["user_id"])
        q1.save()
        return redirect('/userhome')
    return render(request,'addpost.html')

def mypost(request):
    q1=Post.objects.filter(USER_id=request.session["user_id"])
    return render(request,'mypost.html',{'data':q1})

def myprofile(request):
    user_id = request.session.get("user_id")
    q1=User.objects.get(id=user_id)
    return render(request,'myprofile.html',{'data':q1})

def editmyprofile(request,id):
    q1=User.objects.get(id=id)

    if request.method == 'POST':
        Name=request.POST['name']
        Mobile=request.POST['mobile']
        Email=request.POST['email']
        Photo=request.FILES.get('photo')

        if Photo:
            q1.photo=Photo
        q1.name=Name
        q1.mobile=Mobile
        q1.email=Email
        q1.save()

        return redirect('/myprofile')
    return render(request,'editmyprofile.html',{'data':q1})
    

def editpost(request, id):
    q2 = Post.objects.get(id=id)

    if request.method == 'POST':
        Image = request.FILES.get('image')
        Desc = request.POST['description']

        if Image:              
            q2.image = Image

        q2.description = Desc
        q2.save()

        return redirect('/mypost')

    return render(request, 'editpost.html', {'q2': q2})

def deletepost(request,id):
    q2=Post.objects.get(id=id)
    q2.delete()
    return redirect('/mypost')

def addfriend(request):
    user_id = request.session.get("user_id")
    current_user = User.objects.get(id=user_id)

    users = User.objects.exclude(id=user_id)

    final_data = []

    for u in users:
        f = Friends.objects.filter(
            Q(SENDER=current_user, RECEIVER=u) | Q(SENDER=u, RECEIVER=current_user)
        ).first()

        if f:
            print(f.status)
            status = f.status
        else:
            status = "NoRequest"

        final_data.append({
            "user": u,
            "status": status
        })

    return render(request, "addfriend.html", {"data": final_data})

def follow(request, id):
    sender = request.session["user_id"]
    receiver = id

    existing = Friends.objects.filter(SENDER_id=sender, RECEIVER_id=receiver).first()

    if existing:
        if existing.status == "Declined":
            existing.status = "Pending"      
            existing.save()
            messages.success(request, "Follow request sent again!")
            return redirect('/userhome')
        elif existing.status == "Pending":
            messages.error(request, "Request already pending!")
            return redirect('/userhome')
        elif existing.status == "Friends":
            messages.info(request, "You are already friends!")
            return redirect('/userhome')
        else:
            messages.info(request, "Unexpected status!")
            return redirect('/userhome')

    # If no previous request found
    Friends.objects.create(SENDER_id=sender, RECEIVER_id=receiver, status='Pending')
    messages.success(request, "Follow request sent")
    return redirect('/userhome')

def frndrqst(request):
    user_id = request.session["user_id"]
    data=Friends.objects.filter(RECEIVER_id=user_id,status='Pending')
    return render(request,'frndrqst.html',{'data':data})

def followback(request,id):
    q1=Friends.objects.get(id=id)
    q1.status='Friends'
    q1.save()
    return redirect('/myfriends')

def declinerqst(request,id):
    q1=Friends.objects.get(id=id)
    q1.status='Declined'
    q1.save()
    return redirect('/')

def myfriends(request):
    user_id = request.session["user_id"]
    q1 = Friends.objects.filter(
        Q(SENDER_id=user_id, status='Friends') | Q(RECEIVER_id=user_id, status='Friends')
    )

    friends_list = []
    for f in q1:
        if f.SENDER_id == user_id:
            friends_list.append(f.RECEIVER)
        else:
            friends_list.append(f.SENDER)

    return render(request, 'myfriends.html', {'friends': friends_list})

def like(request, id):
    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)    
    post = Post.objects.get(id=id)

    exist_like = Like.objects.filter(USER=user, POST=post)

    if exist_like.exists():
        exist_like.delete()
        return HttpResponse("<script>alert('Unliked');window.location='/userhome'</script>")
    else:
        Like.objects.create(USER=user, POST=post) 
        return HttpResponse("<script>alert('Liked');window.location='/userhome'</script>")



def comment(request, id):
    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)     
    post = Post.objects.get(id=id)          

    if request.method == 'POST':
        cmt = request.POST['comment']
        Comment.objects.create(Comment=cmt, USER=user, POST=post)
        return redirect('/userhome')
    
    q1=Comment.objects.filter(POST=id).order_by('-date_time')
    return render(request,'comment.html',{'data':q1})

def message(request,id):
    user_id = request.session["user_id"]
    Sender=User.objects.get(id=user_id)
    Receiver=User.objects.get(id=id)

    if request.method == 'POST':
        Chat=request.POST['message']
        Message.objects.create(SENDER=Sender,RECEIVER=Receiver,chat=Chat)
        return redirect(f'/message/{id}/')
    q1=Message.objects.filter(
        Q(SENDER=Sender,RECEIVER=Receiver) |
        Q(SENDER=Receiver,RECEIVER=Sender)
    ).order_by('date_time')

    return render(request,'chat.html',{'me':Sender,'friend':Receiver,'chat':q1})
    
    