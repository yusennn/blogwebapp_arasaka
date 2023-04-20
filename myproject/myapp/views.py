from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail

from .forms import UserRegisterForm, UserLoginForm, UserLogoutForm, PostForm
from .models import Post, Registration


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        form = UserLogoutForm(request.POST)
        if form.is_valid():
            logout(request)
            return redirect('login')
    else:
        form = UserLogoutForm()
    return render(request, 'registration/logout.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if form.cleaned_data.get('is_registration_post'):
                post.is_registration_post = True
            post.save()
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def registrations_list(request, event_id):
    registrations = Registration.objects.filter(event_id=event_id)
    return render(request, 'registrations_list.html', {'registrations': registrations})


def create_registration(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registration = Registration(event=event, user=request.user)
    registration.save()

    # send confirmation email to the user
    subject = 'Event Registration Confirmation'
    message = 'Thank you for registering for %s. Your registration was successful.' % event.title
    from_email = 'your_email@example.com'
    to_email = [request.user.email]
    send_mail(subject, message, from_email, to_email)

    return redirect('registrations_list', event_id=event_id)





