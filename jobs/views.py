from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Job
from .forms import JobForm
from django.core.paginator import Paginator
from .models import  JobApplication
from django.contrib import messages


@login_required
def job_list(request):
    jobs = Job.objects.all()

    # Search by job title
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(title__icontains=query)

    # Filter by location
    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(location=location)

    # Filter by company
    company = request.GET.get('company')
    if company:
        jobs = jobs.filter(company=company)

    # Filter by salary range
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')

    if min_salary:
        jobs = jobs.filter(salary__gte=min_salary)
    if max_salary:
        jobs = jobs.filter(salary__lte=max_salary)

    # Get unique locations and companies for dropdown filters
    locations = Job.objects.values_list('location', flat=True).distinct()
    companies = Job.objects.values_list('company', flat=True).distinct()

    # Pagination (5 jobs per page)
    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    return render(request, 'job_list.html', {
        'jobs': jobs_page,
        'locations': locations,
        'companies': companies
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
