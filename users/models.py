from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):
    """Custom user model with email as primary identifier."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})


class Skill(models.Model):
    """Skills that users can have."""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=[
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('business', 'Business'),
        ('marketing', 'Marketing'),
        ('data', 'Data Science'),
        ('other', 'Other'),
    ])
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class UserProfile(models.Model):
    """Extended user profile with additional information."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    university = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    experience_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ], default='beginner')
    interests = models.TextField(max_length=500, blank=True)
    availability = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ], default='available')
    status = models.CharField(max_length=20, choices=[
        ('looking_for_team', 'Looking for Team'),
        ('looking_for_members', 'Looking for Members'),
        ('not_looking', 'Not Looking'),
    ], default='not_looking')
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.user.pk})
    
    class Meta:
        ordering = ['-created_at']
