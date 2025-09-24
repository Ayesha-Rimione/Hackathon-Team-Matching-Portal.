from django.db import models
from django.urls import reverse
from users.models import CustomUser, Skill


class Team(models.Model):
    """Team model for hackathon teams."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    interested_hackathon = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='teams')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(CustomUser, through='TeamMembership', related_name='teams')
    required_skills = models.ManyToManyField(Skill, blank=True)
    max_members = models.PositiveIntegerField(default=5)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
    
    def get_absolute_url(self):
        return reverse('team_detail', kwargs={'pk': self.pk})
    
    def get_member_count(self):
        return self.members.count()
    
    def has_available_slots(self):
        return self.get_member_count() < self.max_members
    
    class Meta:
        ordering = ['-created_at']


class TeamMembership(models.Model):
    """Through model for team membership with roles."""
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[
        ('leader', 'Team Leader'),
        ('member', 'Team Member'),
        ('mentor', 'Mentor'),
    ], default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['team', 'user']
        ordering = ['-joined_at']


class TeamInvitation(models.Model):
    """Team invitation model."""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
    inviter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_invitations')
    invitee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_invitations')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Invitation to {self.team.name} for {self.invitee.email}"
    
    class Meta:
        unique_together = ['team', 'invitee']
        ordering = ['-created_at']


class TeamJoinRequest(models.Model):
    """Team join request model."""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='join_requests')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Join request from {self.user.email} to {self.team.name}"
    
    class Meta:
        unique_together = ['team', 'user']
        ordering = ['-created_at']
