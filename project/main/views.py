from django.db import IntegrityError
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UpdateProfileForm
from django.http import JsonResponse
from .models import User, Competition, Candidate, Vote
from django.contrib.auth.decorators import login_required
from .util import get_client_ip
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
            email = form.cleaned_data['email'].lower()
            print(email)
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)

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
def competition_view(request):
    # Query active competitions
    active_competitions = Competition.objects.filter(
        status='Active').order_by('-start_date')

    # Create lists for trending and other competitions
    trending_competitions = []
    other_competitions = []

    # Loop through competitions and get vote count
    for competition in active_competitions:
        vote_count = Vote.objects.filter(competition=competition).count()
        competition_data = {
            'id': competition.id,
            'name': competition.name,
            'vote_count': vote_count,
            'closing_date': competition.end_date.strftime('%d-%m-%Y')
        }

        # Add the first 2 competitions to trending
        if len(trending_competitions) < 2:
            trending_competitions.append(competition_data)
        else:
            other_competitions.append(competition_data)

    context = {
        'trending_competitions': trending_competitions,
        'other_competitions': other_competitions
    }

    return render(request, 'competition.html', context)


@login_required
def competition_detail_view(request, id):
    # Get the competition by ID
    competition = get_object_or_404(Competition, id=id)

    # Get all candidates for the competition along with their details
    candidates = Candidate.objects.filter(competition=competition)

    context = {
        'competition': competition,
        'candidates': candidates
    }

    return render(request, 'competition_detail.html', context)


@login_required
def vote(request, competition_id, candidate_id):
    # Get the competition and candidate by ID
    competition = get_object_or_404(Competition, id=competition_id)
    candidate = get_object_or_404(
        Candidate, id=candidate_id, competition=competition)

    # Get user IP address
    user_ip = get_client_ip(request)

    # Check if the user has already voted in the competition from this IP
    if Vote.objects.filter(user=request.user, competition=competition).exists() or Vote.objects.filter(ip_address=user_ip, competition=competition).exists():
        messages.error(
            request, "This device has already voted in this competition.")
        return JsonResponse({"message": "This device has already voted"}, status=400)

    try:
        # Record the vote
        Vote.objects.create(
            user=request.user,
            competition=competition,
            candidate=candidate,
            ip_address=user_ip
        )

        # Increase the candidate's total votes
        candidate.total_votes += 1
        candidate.save()

        return JsonResponse({"message": "Successfully voted"}, status=200)
    except IntegrityError:
        return JsonResponse({"message": "An error occurred. Try again."}, status=400)


@login_required
def vote_rules(request):
    return render(request, 'vote_rules.html')


@login_required
def success_vote(request):
    return render(request, 'success_vote.html')


def closed_competitions(request):
    competitions = Competition.objects.filter(status='Inactive')
    return render(request, 'closed_competitions.html', {'competitions': competitions})


def competition_ranking(request, competition_id):

    competition = get_object_or_404(Competition, id=competition_id)

    candidates = Candidate.objects.filter(
        competition=competition).order_by('-total_votes')

    top_3 = candidates[:3]

    other_candidates = candidates[3:]

    return render(request, 'competition_ranking.html', {
        'competition': competition,
        'top_3': top_3,
        'other_candidates': other_candidates
    })
