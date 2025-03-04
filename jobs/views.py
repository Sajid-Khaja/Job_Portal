from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Job
from .forms import JobForm
@login_required
def job_list(request):
    jobs = Job.objects.all()  # Fetch all jobs from the database
    return render(request, 'job_list.html', {'jobs': jobs})
@login_required
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_list')  # Redirect to job listing page
    else:
        form = JobForm()
    
    return render(request, 'job_create.html', {'form': form})
@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'job_detail.html', {'job': job})
@login_required
def job_update(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    
    return render(request, 'job_update.html', {'form': form, 'job': job})
@login_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        job.delete()
        return redirect('job_list')  # Redirect to job listings after deletion

    return render(request, 'job_delete.html', {'job': job})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after signup
            return redirect('job_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('job_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')
