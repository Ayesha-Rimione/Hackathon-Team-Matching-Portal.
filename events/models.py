from django.db import models
from django.urls import reverse
from users.models import CustomUser


class Event(models.Model):
    """Hackathon/tech event model."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    university = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    
    # Event details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    
    # Event settings
    is_online = models.BooleanField(default=False)
    location = models.CharField(max_length=500, blank=True)
    website_url = models.URLField(blank=True)
    registration_url = models.URLField(blank=True)
    
    # Event rules and prizes
    rules = models.TextField(blank=True)
    prizes = models.TextField(blank=True)
    themes = models.TextField(blank=True)
    
    # Status and approval
    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})
    
    def is_registration_open(self):
        from django.utils import timezone
        return timezone.now() <= self.registration_deadline
    
    def is_event_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    def get_participant_count(self):
        return self.participants.count()
    
    class Meta:
        ordering = ['-start_date']


class EventParticipant(models.Model):
    """Event participation model."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='event_participations')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('registered', 'Registered'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('waitlist', 'Waitlist'),
    ], default='registered')
    
    class Meta:
        unique_together = ['event', 'user']
        ordering = ['registration_date']


class EventCategory(models.Model):
    """Event categories for better organization."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # FontAwesome icon class
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Event categories'
        ordering = ['name']


class EventTag(models.Model):
    """Event tags for search and filtering."""
    name = models.CharField(max_length=50, unique=True)
    events = models.ManyToManyField(Event, related_name='tags', blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
