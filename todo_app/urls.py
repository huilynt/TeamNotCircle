"""todo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from todo.views import todo_view, add_todo, delete_todo, archive_todo, team_contributions_view, signup, history_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup, name='signup'),
    path('todo/', todo_view, name='todo_view'),
    path('addTodo/', add_todo, name='add_todo_view'),
    path('deleteTodo/<int:todo_id>/', delete_todo, name='delete_todo_view'),
    path('archiveTodo/<int:todo_id>/', archive_todo, name='archive_todo_view'),
    path('contributions/', team_contributions_view, name='contributions_view'),
    path('historyTodo/', history_view, name="history_view")
]
