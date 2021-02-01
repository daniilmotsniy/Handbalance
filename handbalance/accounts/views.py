from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/account')
        else:
            messages.info(request, 'Username or password is not correct!')

    context = {}
    return render(request, 'accounts/login.html', context)


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/login', messages)

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='login')
def account_page(request):
    context = {}
    return render(request, 'accounts/account.html', context)


@login_required(login_url='login')
def diary_page(request):
    import random

    _blocks = [(f'Block {i + 1}',
                [(f'Ex {j + 10 * i}', str(j + 1 + 10 * i), str(2 * j + 2 + 10 * i)) for j in range(4)]
                ) for i in range(4)]

    blocks = []
    done = []

    for name, tasks in _blocks:
        block = {'name': name, 'tasks': []}
        for task_name, duration, repetitions in tasks:
            block['tasks'].append({'name': task_name, 'duration': duration, 'repetitions': repetitions})
        blocks.append(block)

    return render(request, 'accounts/diary.html', {'blocks': blocks, 'done': done})
