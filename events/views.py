from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import Event, EventParticipant, EventCategory, EventTag
from .serializers import (
    EventSerializer, EventCreateSerializer, EventParticipantSerializer,
    EventParticipantCreateSerializer, EventCategorySerializer, EventTagSerializer
)


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for managing events."""
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_online', 'is_approved', 'is_published', 'university', 'organization']
    search_fields = ['title', 'description', 'themes']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EventCreateSerializer
        return EventSerializer
    
    def get_queryset(self):
        """Filter events based on user permissions."""
        user = self.request.user
        if self.action == 'list':
            # Show approved and published events, or events organized by user
            return Event.objects.filter(
                models.Q(is_approved=True, is_published=True) | 
                models.Q(organizer=user)
            ).distinct()
        return Event.objects.all()
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events."""
        from django.utils import timezone
        now = timezone.now()
        upcoming_events = self.get_queryset().filter(
            start_date__gte=now,
            is_approved=True,
            is_published=True
        ).order_by('start_date')
        
        page = self.paginate_queryset(upcoming_events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ongoing(self, request):
        """Get currently ongoing events."""
        from django.utils import timezone
        now = timezone.now()
        ongoing_events = self.get_queryset().filter(
            start_date__lte=now,
            end_date__gte=now,
            is_approved=True,
            is_published=True
        ).order_by('end_date')
        
        page = self.paginate_queryset(ongoing_events)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(ongoing_events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        """Register for an event."""
        event = self.get_object()
        user = request.user
        
        # Check if user is already registered
        if EventParticipant.objects.filter(event=event, user=user).exists():
            return Response(
                {'error': 'You are already registered for this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if registration is open
        if not event.is_registration_open():
            return Response(
                {'error': 'Registration for this event is closed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if event is full
        if event.max_participants and event.get_participant_count() >= event.max_participants:
            return Response(
                {'error': 'This event is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create participation
        serializer = EventParticipantCreateSerializer(data={
            'event': event.id
        }, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        """Unregister from an event."""
        event = self.get_object()
        user = request.user
        
        try:
            participation = EventParticipant.objects.get(event=event, user=user)
            participation.delete()
            return Response({'message': 'Successfully unregistered from the event.'})
        except EventParticipant.DoesNotExist:
            return Response(
                {'error': 'You are not registered for this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class EventParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing event participants."""
    queryset = EventParticipant.objects.all()
    serializer_class = EventParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Users can see participants for events they're registered for or organizing."""
        user = self.request.user
        return EventParticipant.objects.filter(
            models.Q(user=user) | models.Q(event__organizer=user)
        )


class EventCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing event categories."""
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class EventTagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing event tags."""
    queryset = EventTag.objects.all()
    serializer_class = EventTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
