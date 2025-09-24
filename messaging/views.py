from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message, Notification
from .serializers import (
    ConversationSerializer, ConversationCreateSerializer, MessageSerializer,
    MessageCreateSerializer, NotificationSerializer, NotificationUpdateSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations."""
    queryset = Conversation.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        """Users can only see conversations they're part of."""
        user = self.request.user
        return Conversation.objects.filter(participants=user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark all messages in conversation as read."""
        conversation = self.get_object()
        user = request.user
        
        # Mark messages from other participants as read
        conversation.messages.filter(
            is_read=False
        ).exclude(sender=user).update(is_read=True)
        
        return Response({'message': 'Conversation marked as read.'})


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages."""
    queryset = Message.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def get_queryset(self):
        """Users can only see messages from conversations they're part of."""
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
    
    def perform_create(self, serializer):
        """Create message and update conversation timestamp."""
        message = serializer.save()
        conversation = message.conversation
        conversation.save()  # This updates the updated_at field
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a message as read."""
        message = self.get_object()
        user = request.user
        
        # Only mark as read if user is not the sender
        if message.sender != user:
            message.is_read = True
            message.save()
            return Response({'message': 'Message marked as read.'})
        
        return Response(
            {'error': 'You cannot mark your own messages as read.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing notifications."""
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return NotificationSerializer
    
    def get_queryset(self):
        """Users can only see their own notifications."""
        user = self.request.user
        return Notification.objects.filter(user=user)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read."""
        user = request.user
        user.notifications.filter(is_read=False).update(is_read=True)
        return Response({'message': 'All notifications marked as read.'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications."""
        user = request.user
        count = user.notifications.filter(is_read=False).count()
        return Response({'unread_count': count})
