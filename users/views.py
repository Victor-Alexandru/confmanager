from django.shortcuts import render,redirect
from confsite import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .forms import RegisterForm,LoginForm
from django.contrib import messages
# Create your views here.


def register_view(request):
    if request.method=='POST':
        process_register(request)
        return redirect('confsite-index')
    form=RegisterForm()
    return render(request,'users/register-form.html',{'form':form})


def login_view(request):
    if request.method=='POST':
        process_login(request)
        return redirect('confsite-index')
    form=LoginForm()
    return render(request,'users/login-form.html',{'form': form})


def process_register(data):
    email=data.POST.get("email")
    name=data.POST.get("name")
    password=data.POST.get("password")
    website=data.POST.get("website")
    affiliation=data.POST.get("affiliation")
    register_as=data.POST.get("register_as")

    if register_as=="Steering":
        User.objects.create_user(username=email, password=password,email="steering@steering")
        models.Login.objects.create(email=email, password=password)
        models.SteeringCommittee.objects.create(email=models.Login.objects.filter(email=email)[0],name=name,website=website,affiliation=affiliation)
        messages.success(data,f'Steering account succesfully created!')
    else:
        User.objects.create_user(username=email, password=password,email="participant@participant")
        models.Login.objects.create(email=email, password=password)
        models.Participant.objects.create(email=models.Login.objects.filter(email=email)[0],name=name,website=website,affiliation=affiliation)
        messages.success(data,f'Participant account succesfully created!')


def process_login(data):
    email=data.POST.get("email")
    password=data.POST.get("password")
    login_as=data.POST.get("login_as")
    loginUser=models.Login.objects.filter(email=email)
    if loginUser:
        loginUser=loginUser[0]
    else:
        messages.error(data,'Email does not have an account associated with it!')
        return
    user=authenticate(username=email,password=password)
    if user is not None:
        if login_as=="Steering":
            sc=models.SteeringCommittee.objects.filter(email=loginUser)
            if not sc:
                messages.error(data,'Invalid account type!')
                return
            login(request=data,user=user)
            messages.success(data,'You are now logged in!')
        else:
            pc=models.Participant.objects.filter(email=loginUser)
            if not pc:
                messages.error(data,'Invalid account type!')
                return
            login(request=data,user=user)
            messages.success(data,'You are now logged in!')
    else:
        messages.error(data,'Invalid password!')
