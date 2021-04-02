import operator

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .models import TaskList, TaskBlock
from django.utils import timezone


# count of tasks in one block
_tasks_per_block = 5


def login_page(request):
    """ Login logic """
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
    """ Register logic """
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
    """ Logout logic """
    logout(request)
    return redirect('/login')


@login_required(login_url='login')
def account_page(request):
    """ This func allows define which block will be shown by 'start training' btn """
    link_to_block = 0
    paid = False
    try:
        balance = TaskList.objects.get(user=request.user).balance
        paid = TaskList.objects.get(user=request.user).paid
        link_to_block = 'block' + str(int(balance/5))
    except TaskList.DoesNotExist:
        balance = 0

    return render(request, 'accounts/account.html', {'link_to_block': link_to_block, 'paid': paid})


def leaders(request):
    """ Leaders page logic """
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
    """ Main logic of 'training dairy' """

    # information will be shown on all blocks
    # _blocks = [(f'Block {i + 1}',
    #             [(f'Ex {j + 5 * i}', str(j + 1 + 5 * i), str(2 * j + 2 + 5 * i)) for j in range(_tasks_per_block)]
    #             ) for i in range(5)]

    _blocks = [('Block 1', [('Warm up', '120', '1'), ('Floor', '60', '1'), ('Chair', '60', '2'), ('Wall stand', '30', '4')]),
               ('Block 2', [('Ex 6', '6', '7'), ('Ex 66', '7', '9'), ('Ex 7', '8', '11'), ('Ex 8', '9', '13'),
                                                                ('Ex 9', '10', '15')]),
               ('Block 3', [('Ex 10', '11', '12'), ('Ex 11', '12', '14'), ('Ex 12', '13', '16'),
                            ('Ex 13', '14', '18'), ('Ex 14', '15', '20')]),
               ('Block 4', [('Ex 15', '16', '17'), ('Ex 16', '17', '19'), ('Ex 17', '18', '21'), ('Ex 18', '19', '23'),
                            ('Ex 19', '20', '25')]),
               ('Block 5', [('Ex 20', '21', '22'), ('Ex 21', '22', '24'), ('Ex 22', '23', '26'), ('Ex 23', '24', '28'),
                                                                  ('Ex 24', '25', '30')])]

    try:
        task_list = TaskList.objects.get(user=request.user)
        balance = task_list.balance
    except TaskList.DoesNotExist:
        balance = 0

    try:
        done_tasks = {t.block_id: [bool(t.tasks & 1 << i) for i in range(t.tasks_count)]
                      for t in sorted(TaskBlock.objects.filter(user=request.user), key=lambda b: b.block_id)}
        done_tasks = {k: list(v) for k, v in done_tasks.items()}
    except TaskBlock.DoesNotExist:
        done_tasks = {}

    # last login logic
    try:
        last_login_date = request.user.last_login.date()
        print(last_login_date)
    except TaskBlock.DoesNotExist:
        last_login = ''

    blocks = []
    done = []

    for block_id, (name, tasks) in enumerate(_blocks):
        block_done_tasks = done_tasks.get(block_id, [False] * _tasks_per_block)
        block_tasks = []
        block_done = []
        for task_id, ((task_name, duration, repetitions), task_done) in enumerate(zip(tasks, block_done_tasks)):
            task = {'name': task_name, 'duration': duration, 'repetitions': repetitions,
                    'block_id': block_id, 'id': task_id}

            (block_done if task_done else block_tasks).append(task)

        if block_tasks:
            blocks.append({'name': name, 'tasks': block_tasks, 'id': block_id})
        if block_done:
            done.append(block_done)

    return render(request, 'accounts/diary.html', {'blocks': blocks, 'done': done, 'balance': balance,})


@login_required(login_url='login')
def complete_task(request, block_id, task_id):
    """ Moves task to the 'done tasks' """
    try:
        block = TaskBlock.objects.get(user=request.user, block_id=block_id)

        block.tasks |= 1 << task_id

        block.save()
    except TaskBlock.DoesNotExist:
        TaskBlock(user=request.user, block_id=block_id, tasks=1 << task_id, tasks_count=_tasks_per_block)

    try:
        done_tasks = TaskList.objects.get(user=request.user)

        done_tasks.balance += 1

        done_tasks.save()
    except TaskList.DoesNotExist:
        TaskList(user=request.user, balance=1).save()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def complete_block(request, block_id):
    """ Moves block to the 'done tasks' """
    try:
        block = TaskBlock.objects.get(user=request.user, block_id=block_id)

        tasks_done = sum(not block.tasks & 1 << i for i in range(block.tasks_count))

        block.tasks = (1 << block.tasks_count) - 1

        block.save()
    except TaskBlock.DoesNotExist:
        TaskBlock(user=request.user, block_id=block_id,
                  tasks=(1 << _tasks_per_block) - 1, tasks_count=_tasks_per_block).save()
        tasks_done = _tasks_per_block

    try:
        done_tasks = TaskList.objects.get(user=request.user)

        done_tasks.balance += tasks_done

        done_tasks.save()
    except TaskList.DoesNotExist:
        TaskList(user=request.user, balance=tasks_done).save()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def return_task(request, block_id, task_id):
    """ Moves task back to the block """
    try:
        done_tasks = TaskList.objects.get(user=request.user)
        block = TaskBlock.objects.get(user=request.user, block_id=block_id)

        block.tasks ^= 1 << task_id

        done_tasks.balance -= 1

        done_tasks.save()
        block.save()
    except (TaskList.DoesNotExist, TaskBlock.DoesNotExist):
        return HttpResponseBadRequest()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def return_block(request, block_id):
    """ Moves block back """
    try:
        done_tasks = TaskList.objects.get(user=request.user)
        block = TaskBlock.objects.get(user=request.user, block_id=block_id)

        tasks_returned = sum(bool(block.tasks & 1 << i) for i in range(block.tasks_count))

        block.tasks = 0

        done_tasks.balance -= tasks_returned

        done_tasks.save()
        block.save()
    except (TaskList.DoesNotExist, TaskBlock.DoesNotExist):
        return HttpResponseBadRequest()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def return_all_tasks(request):
    """ Moves all blocks back """
    try:
        done_tasks = TaskList.objects.get(user=request.user)
        blocks = TaskBlock.objects.filter(user=request.user)

        for block in blocks:
            block.tasks = 0
            block.save()

        done_tasks.balance = 0

        done_tasks.save()
    except (TaskList.DoesNotExist, TaskBlock.DoesNotExist):
        return HttpResponseBadRequest()

    return HttpResponseRedirect('/diary')


@login_required(login_url='login')
def buy(request):
    """ Payment process simulating """
    try:
        user = TaskList.objects.get(user=request.user)
        user.paid = True
        user.save()
    except TaskList.DoesNotExist:
        return HttpResponseBadRequest()
    return redirect('/account')