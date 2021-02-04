import operator

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .models import TaskList
from django.utils import timezone


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


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='login')
def account_page(request):
    context = {}
    return render(request, 'accounts/account.html', context)


def leaders(request):
    try:
        info = TaskList.objects.all()
        raw = {}
        for i in info:
            raw[str(i.user)] = i.balance
        users = dict(sorted(raw.items(), key=operator.itemgetter(1), reverse=True))
    except TaskList.DoesNotExist:
        users = {}
    return render(request, 'accounts/leaders.html', {'users': users})


# Diary page
@login_required(login_url='login')
def diary_page(request):
    _blocks = [(f'Block {i + 1}',
                [(f'Ex {j + 10 * i}', str(j + 1 + 10 * i), str(2 * j + 2 + 10 * i)) for j in range(4)]
                ) for i in range(4)]

    try:
        done_tasks = TaskList.objects.get(user=request.user).tasks
        available_for_editing = False
        if TaskList.objects.get(user=request.user).last_activity != timezone.now().date():
            available_for_editing = True
    except TaskList.DoesNotExist:
        done_tasks = 0
        available_for_editing = False

    blocks = []
    done = []

    for block_id, (name, tasks) in enumerate(_blocks):
        block_tasks = []
        for task_id, (task_name, duration, repetitions) in enumerate(tasks):
            task_id = task_id + 4 * block_id

            task = {'name': task_name, 'duration': duration, 'repetitions': repetitions, 'id': task_id}

            if done_tasks & (1 << task_id):
                task['block'] = block_id + 1
                done.append(task)
            else:
                block_tasks.append(task)

        if block_tasks:
            blocks.append({'name': name, 'tasks': block_tasks, 'id': block_id})

    try:
        balance = TaskList.objects.get(user=request.user).balance
    except TaskList.DoesNotExist:
        balance = 0

    return render(request, 'accounts/diary.html', {'blocks': blocks, 'done': done, 'balance': balance,
                                                   'available_for_editing': available_for_editing})


@login_required(login_url='login')
def complete_task(request, task_id):
    try:
        done_tasks = TaskList.objects.get(user=request.user)

        done_tasks.tasks |= 1 << task_id

        done_tasks.balance += 1

        done_tasks.save()

    except TaskList.DoesNotExist:
        TaskList(user=request.user, tasks=1 << task_id).save()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def complete_block(request, block_id):
    try:
        done_tasks = TaskList.objects.get(user=request.user)

        done_tasks.tasks |= 0b1111 << 4 * block_id

        done_tasks.balance += 1

        done_tasks.last_activity = timezone.now().date()

        done_tasks.save()

    except TaskList.DoesNotExist:
        TaskList(user=request.user, tasks=0b1111 << 4 * block_id).save()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def return_task(request, task_id):
    try:
        done_tasks = TaskList.objects.get(user=request.user)

        done_tasks.tasks ^= 1 << task_id

        done_tasks.balance -= 1
        done_tasks.last_activity = '2000-04-20'

        done_tasks.save()
    except TaskList.DoesNotExist:
        return HttpResponseBadRequest()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def return_all_tasks(request):
    try:
        done_tasks = TaskList.objects.get(user=request.user)

        done_tasks.tasks = 0
        
        done_tasks.last_activity = '2000-04-20'

        done_tasks.save()
    except TaskList.DoesNotExist:
        return HttpResponseBadRequest()
    return HttpResponseRedirect('/diary')
