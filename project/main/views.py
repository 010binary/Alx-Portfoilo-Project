from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse
from .forms import RegisterForm, LoginForm, UpdateProfileForm
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
    return redirect('index')


def vote_rules(request):
    return render(request, 'vote_rules.html')


def success_vote(request):
    return render(request, 'success_vote.html')


@login_required
def profile(request):
    user_data = request.user

    form = UpdateProfileForm(initial={
        'name': user_data.name,
        'username': user_data.username,
        'mobile_no': user_data.mobile_no,
        'email': user_data.email,
        'address': user_data.address,
    })

    return render(request, 'profile.html', {'form': form, 'user_data': user_data})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)

        if form.is_valid():
            # Get the logged-in user
            user = request.user

            # Update the user's fields from the form's cleaned data
            user.name = form.cleaned_data['name']
            user.username = form.cleaned_data['username']
            user.mobile_no = form.cleaned_data['mobile_no']
            user.email = form.cleaned_data['email']
            # This can be None/blank
            user.address = form.cleaned_data['address']

            # Save the updated user data
            user.save()

            # Redirect to profile page after successful update
            return redirect('profile')

    else:
        # If not a POST request, just render the form
        form = UpdateProfileForm(initial={
            'name': request.user.name,
            'username': request.user.username,
            'mobile_no': request.user.mobile_no,
            'email': request.user.email,
            'address': request.user.address,
        })

    return render(request, 'profile.html', {'form': form})


@login_required
def get_all_competition():
