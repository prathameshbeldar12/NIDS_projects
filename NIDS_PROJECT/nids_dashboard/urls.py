from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_csv, name='upload'),

    path('logs/', views.attack_logs, name='logs'),
    path('stats/', views.attack_stats, name='stats'),
    path('about/', views.about_page, name='about'),

    path('delete/<int:id>/', views.delete_detection, name='delete_detection'),

    path('forgot/', views.forgot_password, name='forgot'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
