from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Page
import random
from django.contrib.auth.decorators import login_required

def home_page(request):
    return render(request, template_name='home.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, template_name='register.html', context={'error': 'Username already exists'})
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                return redirect('login')

    return render(request, template_name='register.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, template_name='login.html', context={'error': 'Invalid username or password'})
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def create_page(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        context = request.POST.get('context')

        Page.objects.create(
            title=title,
            context=context,
            author=request.user
        )


    return render(request, template_name='create_page.html')


def all_pages(request):
    pages = Page.objects.all()
    if request.GET.get('q', False):
        pages = Page.objects.filter(title__icontains=request.GET.get('q'))
    return render(request, template_name='all_pages.html', context={'pages': pages})


def detail_page(request, page_id):
    page = Page.objects.get(id=page_id)
    context = {"page": page}
    return render(request, 'detail_page.html', context=context)

@login_required(login_url='login')
def delete_page(request, page_id):
    page = Page.objects.get(id=page_id)
    page.delete()
    return redirect('all_pages')

@login_required(login_url='login')
def edit_page(request, page_id):
    page = Page.objects.get(id=page_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        page.title = title
        page.context = content
        page.save()
        return redirect('all_pages')
    return render(request, template_name='edit_page.html', context={'page': page})


def random_page(request):
    page = random.choice(Page.objects.all())
    return render(request, template_name='detail_page.html', context={'page': page})

