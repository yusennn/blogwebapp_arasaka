from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserLogoutForm, PostForm, EventForm
from .models import Post, Event, EventVisitor


def home(request):
    posts = Post.objects.all()
    latest_post = Post.objects.order_by('-created_at').first()
    latest_event = Event.objects.order_by('-created_at').first()
    latest_events = Event.objects.order_by('-created_at')[:3]
    latest_posts = Post.objects.order_by('-created_at')[:3]
    context = {'posts': posts, 'latest_post': latest_post, 'latest_event': latest_event, 'latest_events': latest_events, 'latest_posts': latest_posts}
    return render(request, 'blog/home.html', context)


def event_list(request):
    events = Event.objects.order_by('-created_at')
    return render(request, 'blog/events.html', {'events': events})


def post_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog/posts.html', {'posts': posts})


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


@permission_required('myapp.can_create_post')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/base.html', {'form': form})


@permission_required('myapp.can_create_event')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'blog/base.html', {'form': form})


@login_required
def event_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # проверяем, существует ли уже запись на это событие для текущего пользователя
    try:
        visitor = EventVisitor.objects.get(event=event, user=request.user)
    except EventVisitor.DoesNotExist:
        # если записи нет, то создаем новую запись
        visitor = EventVisitor.objects.create(event=event, name=request.user.username, email=request.user.email, user=request.user)

    return render(request, 'event_registration.html', {'event': event, 'visitor': visitor})




















