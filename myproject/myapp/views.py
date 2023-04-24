from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserLogoutForm, PostForm, EventRegistrationForm
from .models import Post, Event, EventVisitor


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def event_list(request):
    events = Event.objects.all()
    return render(request, 'blog/events.html', {'events': events})


def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'blog/event_detail.html', {'event': event})


def delete_event(pk):
    post = get_object_or_404(Event, pk=pk)
    post.delete()
    return redirect('home')


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def delete_post(pk):
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


def event_registration(request, pk):
    print("view is being called")
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, event=event) # pass the event instance
        if form.is_valid():
            event_visitor = form.save(commit=True)
            print(form.errors)
            print(event_visitor)
            event_visitor.event = event
            event_visitor.save()
            messages.success(request, 'You have successfully registered for the event!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventRegistrationForm(event=event) # pass the event instance
    return render(request, 'event_registration.html', {'form': form, 'event': event})











