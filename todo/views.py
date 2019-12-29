from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import TodoItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
@login_required
def todo_view(request):
    print(request.user)
    all_todo_items = TodoItem.objects.filter(user=request.user, deleted=False)
    return render(request, 'todo.html', {'all_items': all_todo_items})


@login_required
def add_todo(request):
    new_item = TodoItem(content=request.POST['content'], user=request.user)
    new_item.save()
    return HttpResponseRedirect('/todo/')


@login_required
def delete_todo(request, todo_id):
    item_to_delete = TodoItem.objects.get(id=todo_id)
    item_to_delete.deleted = True
    item_to_delete.save()
    return HttpResponseRedirect('/todo/')


@login_required
def archive_todo(request, todo_id):
    item_to_archive = TodoItem.objects.get(id=todo_id)
    item_to_archive.archive = True
    item_to_archive.save()
    return HttpResponseRedirect('/todo/')


def team_contributions_view(request):
    return render(request, 'contributions.html')


def signup(request):
    if request.method == 'POST':
        print('post')
        form = UserCreationForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print('valid signup')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/todo/')
        else:
            print(form.errors)

    else:
        print('else')
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def history_view(request):
    added_history = TodoItem.objects.filter(archive=True)
    return render(request, 'history.html',
                  {'todo_item_history': added_history})
