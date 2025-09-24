from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('teams/', views.teams, name='teams'),
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/<int:pk>/', views.team_detail, name='team_detail'),
    path('teams/<int:pk>/requests/', views.team_requests, name='team_requests'),
    path('teams/<int:pk>/requests/<int:req_id>/<str:action>/', views.team_request_action, name='team_request_action'),
    path('events/', views.events, name='events'),
    path('messaging/', views.messaging, name='messaging'),
    path('messages/inbox/', views.messages_inbox, name='messages_inbox'),
    path('messages/send/<int:user_id>/', views.message_send, name='message_send'),
    path('api/test/', views.api_test, name='api_test'),
]
