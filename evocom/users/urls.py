from django.urls import path
from . import views

app_name = 'users' 
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_page, name='login'),
    path('loginfn/', views.login_view, name='loginfn'),
    path('logout/', views.user_logout, name='logout'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('member_index/', views.member_index, name='member_index'),
    path('community_admin_index/', views.community_admin_index, name='community_admin_index'),
    path('forgot_password/', views.password_reset_request, name='password_reset_request'),
    path('reset_password/<str:token>/', views.reset_password, name='reset_password'),
    path('select_user_type/', views.select_user_type, name='select_user_type'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('updateprofile/', views.update_profile, name='update_profile'),
    path('passwordchange/', views.password_change, name='password_change'),
    path('check-unique/', views.check_unique, name='check_unique'),
]
