from django.urls import path
import airq.views

urlpatterns = [
    path('',airq.views.home,name='home'),
    path('home',airq.views.home,name='home'),
    path('register_admin',airq.views.register_admin,name='register_admin'),
    path('register_user',airq.views.register_user,name='register_user'),
    path('update_pr_usr', airq.views.update_pr_usr, name='update_pr_usr'),
    path('register_recruiter',airq.views.register_recruiter,name='register_recruiter'),
    path('login',airq.views.login,name='login'),
    path('admin_home',airq.views.admin_home,name='admin_home'),
    path('user_home',airq.views.user_home,name='user_home'),
    path('recruiter_home',airq.views.recruiter_home,name='recruiter_home'),
    path('predict_job_usr', airq.views.predict_job_usr, name='predict_job_usr'),
    path('logout',airq.views.logout,name='logout'),
    path('job_posts_recr', airq.views.job_posts_recr, name='job_posts_recr'),
    path('add_job_recr', airq.views.add_job_recr, name='add_job_recr'),
]