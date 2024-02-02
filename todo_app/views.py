from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task
from .forms import *  # Make sure to import TaskForm
from django.contrib.auth.views import LoginView


from django.contrib.auth.views import LoginView, LogoutView

from django.utils import timezone
from datetime import date


def handling_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('tasks')

def custom_logout(request):
    logout(request)
    return redirect('login')



def register_page(request):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    success_url = reverse('tasks')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return redirect(success_url)
    else:
        form = form_class()

    if request.user.is_authenticated:
        return redirect('tasks')

    return render(request, template_name, {'form': form})

@login_required
@login_required
def task_list(request):
    template_name = 'base/task_list.html'
    tasks = Task.objects.filter(user=request.user)
    count = tasks.filter(complete=False).count()

    # New: Get upcoming tasks and overdue tasks
    upcoming_tasks = tasks.filter(due_date__gte=date.today()).order_by('due_date')
    overdue_tasks = tasks.filter(due_date__lt=date.today(), complete=False).order_by('-due_date')

    search_input = request.GET.get('search-area') or ''
    if search_input:
        tasks = tasks.filter(title__contains=search_input)

    return render(request, template_name, {
        'tasks': tasks,
        'count': count,
        'search_input': search_input,
        'upcoming_tasks': upcoming_tasks,
        'overdue_tasks': overdue_tasks,
    })
    
    
    

@login_required
def task_detail(request, pk):
    template_name = 'base/task.html'
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, template_name, {'task': task})

@login_required
def task_create(request):
    template_name = 'base/task_form.html'
    success_url = reverse('tasks')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(success_url)
    else:
        form = TaskForm()

    return render(request, template_name, {'form': form})

@login_required
def task_update(request, pk):
    template_name = 'base/task_form.html'
    success_url = reverse('tasks')
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = TaskForm(instance=task)

    return render(request, template_name, {'form': form})

@login_required
def task_delete(request, pk):
    template_name = 'base/task_confirm_delete.html'
    success_url = reverse('tasks')
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect(success_url)

    return render(request, template_name, {'task': task})

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                request.user.set_task_order(positionList)

        return redirect(reverse('tasks'))
