from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Job,Job, JobApplication, Bookmark
from .forms import JobForm
from django.core.paginator import Paginator
from .models import  JobApplication
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User


@login_required


def job_list(request):
    jobs = Job.objects.all()

    # Extract unique locations and companies from the database
    locations = Job.objects.values_list('location', flat=True).distinct()
    companies = Job.objects.values_list('company', flat=True).distinct()

    # Filtering logic
    if request.GET.get("q"):
        jobs = jobs.filter(title__icontains=request.GET["q"])

    if request.GET.get("location"):
        jobs = jobs.filter(location=request.GET["location"])

    if request.GET.get("company"):
        jobs = jobs.filter(company=request.GET["company"])

    if request.GET.get("min_salary"):
        jobs = jobs.filter(salary__gte=request.GET["min_salary"])

    if request.GET.get("max_salary"):
        jobs = jobs.filter(salary__lte=request.GET["max_salary"])

    return render(request, "job_list.html", {
        "jobs": jobs,
        "locations": locations,
        "companies": companies
    })
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Check if the user has already applied
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', job.id)

    # Save the application
    JobApplication.objects.create(user=request.user, job=job)
    messages.success(request, "You have successfully applied for this job!")

    return redirect('job_detail', job.id)
@login_required
def application_status(request):
    applications = JobApplication.objects.filter(user=request.user).select_related('job')
    return render(request, 'application_status.html', {'applications': applications})

@login_required
def application_history(request):
    applications = JobApplication.objects.filter(user=request.user).select_related('job')

    return render(request, 'application_history.html', {'applications': applications})
@login_required
def applied_jobs(request):
    applied_jobs = JobApplication.objects.filter(user=request.user).select_related('job')
    return render(request, 'applied_jobs.html', {'applied_jobs': applied_jobs})
def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required)
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
@user_passes_test(admin_required)
@login_required
def registered_users(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'registered_users.html', {'users': users})




@login_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, job=job)

    if created:
        messages.success(request, "Job saved successfully!")
    else:
        messages.info(request, "This job is already in your saved list.")

    return redirect('job_list')  # Redirect to job listings

@login_required
def saved_jobs(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('job')
    return render(request, 'saved_jobs.html', {'bookmarks': bookmarks})

@login_required
def remove_saved_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    bookmark = Bookmark.objects.filter(user=request.user, job=job)
    
    if bookmark.exists():
        bookmark.delete()
        messages.success(request, "Job removed from saved jobs.")
    else:
        messages.error(request, "This job is not in your saved list.")

    return redirect('saved_jobs')