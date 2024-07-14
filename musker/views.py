from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Profile
from .forms import TweetForm, SignUpForm
from .models import tweet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweeti = form.save(commit=False)
                tweeti.user = request.user
                tweeti.save()
                messages.success(request, ("Tweet postado!"))
                return redirect('home')
        tweets = tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"tweets":tweets, "form":form})
    else:
        tweets = tweet.objects.all().order_by("-created_at")  
        return render(request, 'home.html', {"tweets":tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user = request.user)
        return render(request,'profile_list.html', {"profiles":profiles} )
    else:
        messages.success(request, ("Você deve estar logado.."))
        return redirect('home')

def profile(request, pk):
     if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        tweets = tweet.objects.filter(user_id = pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        return render(request, 'profile.html', {'profile':profile, "tweets":tweets})
     else:
        messages.success(request, ("Você deve estar logado.."))
        return redirect('home')
     
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Você está logado."))
            return redirect('home')
        else:
            messages.success(request, ("Usuário ou senha não encontrados"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Usuário deslogado"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Usuário cadastrado"))
            return redirect('home')
    return render(request, 'register.html', {'form':form})