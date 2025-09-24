from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'invitations', views.TeamInvitationViewSet, basename='invitation')
router.register(r'join-requests', views.TeamJoinRequestViewSet, basename='join-request')

urlpatterns = [
    path('', include(router.urls)),
]
