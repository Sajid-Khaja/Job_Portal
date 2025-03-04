from django.urls import path
from .views import (
    job_list, job_create, job_detail, job_update, job_delete, 
    register, user_login, user_logout,apply_job,application_history,application_status,applied_jobs,registered_users,save_job, saved_jobs, remove_saved_job
)

urlpatterns = [
    path('', job_list, name='job_list'),
    path('post-job/', job_create, name='job_create'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('job/<int:job_id>/edit/', job_update, name='job_update'),
    path('job/<int:job_id>/delete/', job_delete, name='job_delete'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('jobs/<int:job_id>/apply/', apply_job, name='apply_job'),
    path('applications/', application_history, name='application_history'),
     path('my-applications/', application_status, name='application_status'),
      path('applied-jobs/', applied_jobs, name='applied_jobs'),
      path('registered-users/', registered_users, name='registered_users'),
     path('save-job/<int:job_id>/', save_job, name='save_job'),
    path('saved-jobs/', saved_jobs, name='saved_jobs'),
    path('remove-saved-job/<int:job_id>/', remove_saved_job, name='remove_saved_job'),
]  

