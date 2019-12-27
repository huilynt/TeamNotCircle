from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TodoItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def todo_view(request):
    all_todo_items = TodoItem.objects.filter(archive=False)
    return render(request, 'todo.html', {'all_items': all_todo_items})


@login_required
def add_todo(request):
    new_item = TodoItem(content=request.POST['content'])
    new_item.save()
    request.session['new_item'] = new_item.content
    return HttpResponseRedirect('/todo/')


@login_required
def delete_todo(request, todo_id):
    item_to_delete = TodoItem.objects.get(id=todo_id)
    item_to_delete.delete()
    return HttpResponseRedirect('/todo/')


@login_required
def archive_todo(request, todo_id):
    item_to_archive = TodoItem.objects.get(id=todo_id)
    item_to_archive.archive = True
    item_to_archive.save()
    return HttpResponseRedirect('/todo/')

def team_contributions_view(request):
    return render(request, 'contributions.html')

@login_required
def history_view(request):
    todo_history = []
    item_added = request.session.get('new_item', None)
    todo_history.append(item_added) 
    return render(request, 'history.html', {'todo_item_history': todo_history})