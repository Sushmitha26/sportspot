from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = "login"),
    path('signup/', views.signup, name = "signup"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('dashboard/mentors', views.mentors, name = "mentors"),
    path('dashboard/events', views.events, name = "events"),
    path('dashboard/gallery', views.gallery, name = "gallery"),
    path('dashboard/shortlisted', views.shortlisted, name = "shorlisted"),
    path('logout/', views.logout, name = "logout")
]