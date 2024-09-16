from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.http import JsonResponse
# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print(form.cleaned_data)
            return redirect('index')
        else:
            print("Form is not valid")
            print(form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'registration.html', context=context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print(form.cleaned_data)
            return redirect('index')
        else:
            print("Form is not valid")
            print(form.errors)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'login.html', context=context)
