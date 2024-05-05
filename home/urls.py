from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home),
    path('anasayfa', views.home),
    path('relatives', views.relatives, name='relatives'),
    path('questionary', views.questionary, name='questionary'),
    path('profile', views.profile, name='profile'),
    path('daily-table', views.daily_table, name='daily-table'),
    path('get-hes-code', views.get_hes_code, name='get-hes-code'),
    path('covidinfo', views.covidinfo, name='covidinfo'),
    path('passport', views.passport, name='passport'),
    path('report', views.report, name='report'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('deleterelative', views.deleterelative, name='deleterelative'),
]