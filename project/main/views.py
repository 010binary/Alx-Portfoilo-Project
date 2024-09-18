from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
from .models import User
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def steps(request):
    return render(request, 'steps.html')


def register(request):
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = User.objects.create_user(
                    email=cleaned_data['email'],
                    username=cleaned_data['username'],
                    name=cleaned_data['name'],
                    mobile_no=cleaned_data['mobile'],
                    password=cleaned_data['password']
                )
                print("user created", user)
                return JsonResponse({'status': 'success', 'message': 'Registration successful', 'redirect': reverse('index')})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        except IntegrityError as e:
            return JsonResponse({'status': 'error', 'message': 'Username or email or mobile already exists'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                print("User logged in", user)
                return JsonResponse({'status': 'success', 'message': 'Login successful', 'redirect': reverse('index')})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid email or password'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success', 'message': 'Logout successful', 'redirect': reverse('login')})


def vote_rules(request):
    return render(request, 'vote_rules.html')


def success_vote(request):
    return render(request, 'success_vote.html')


@login_required
def profile(request):
    user_data = User.objects.get(id=request.user.id)
    return render(request, 'profile.html', {'user_data': user_data})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user  # Assuming user is logged in
        user.name = request.POST['name']
        user.username = request.POST['username']
        user.mobile_no = request.POST['mobile_no']
        user.email = request.POST['email']
        user.address = request.POST['address']
        user.save()
        return redirect('profile')
    return render(request, 'profile.html')
