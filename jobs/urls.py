from django.urls import path
from .views import (
    job_list, job_create, job_detail, job_update, job_delete, 
    register, user_login, user_logout
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
]
