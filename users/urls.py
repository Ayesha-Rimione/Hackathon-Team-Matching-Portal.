from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'skills', views.SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
