from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import TodoItem


# Create your views here.
def todo_view(request):
    all_todo_items = TodoItem.objects.filter(archive=False)
    return render(request, 'todo.html', {'all_items': all_todo_items})


def add_todo(request):
    new_item = TodoItem(content=request.POST['content'])
    new_item.save()
    return HttpResponseRedirect('/todo/')


def delete_todo(request, todo_id):
    item_to_delete = TodoItem.objects.get(id=todo_id)
    item_to_delete.delete()
    return HttpResponseRedirect('/todo/')


def archive_todo(request, todo_id):
    item_to_archive = TodoItem.objects.get(id=todo_id)
    item_to_archive.archive = True
    item_to_archive.save()
    return HttpResponseRedirect('/todo/')