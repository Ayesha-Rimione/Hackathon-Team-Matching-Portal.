from django.db import models
from users.models import CustomUser


class Conversation(models.Model):
    """Conversation between users."""
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        participant_names = ', '.join([p.email for p in self.participants.all()[:3]])
        return f"Conversation: {participant_names}"
    
    class Meta:
        ordering = ['-updated_at']


class Message(models.Model):
    """Individual message in a conversation or direct message between users."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"
    
    class Meta:
        ordering = ['created_at']


class Notification(models.Model):
    """User notifications."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('team_invitation', 'Team Invitation'),
        ('join_request', 'Join Request'),
        ('event_update', 'Event Update'),
        ('message', 'New Message'),
        ('general', 'General'),
    ], default='general')
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.email}: {self.title}"
    
    class Meta:
        ordering = ['-created_at']
