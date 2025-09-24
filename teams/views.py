from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Team, TeamMembership, TeamInvitation, TeamJoinRequest
from .serializers import (
    TeamSerializer, TeamCreateSerializer, TeamInvitationSerializer,
    TeamInvitationCreateSerializer, TeamJoinRequestSerializer,
    TeamJoinRequestCreateSerializer
)
from django.db import models


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for managing teams."""
    queryset = Team.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeamCreateSerializer
        return TeamSerializer
    
    def get_queryset(self):
        """Filter teams based on user permissions."""
        user = self.request.user
        if self.action == 'list':
            # Show public teams and teams user is member of
            return Team.objects.filter(
                models.Q(is_public=True) | models.Q(members=user)
            ).distinct()
        return Team.objects.all()
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Request to join a team."""
        team = self.get_object()
        user = request.user
        
        # Check if user is already a member
        if team.members.filter(id=user.id).exists():
            return Response(
                {'error': 'You are already a member of this team.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if team has available slots
        if not team.has_available_slots():
            return Response(
                {'error': 'Team is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create join request
        serializer = TeamJoinRequestCreateSerializer(data={
            'team': team.id,
            'message': request.data.get('message', '')
        }, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team."""
        team = self.get_object()
        user = request.user
        
        try:
            membership = TeamMembership.objects.get(team=team, user=user)
            membership.delete()
            return Response({'message': 'Successfully left the team.'})
        except TeamMembership.DoesNotExist:
            return Response(
                {'error': 'You are not a member of this team.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TeamInvitationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing team invitations."""
    queryset = TeamInvitation.objects.all()
    serializer_class = TeamInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeamInvitationCreateSerializer
        return TeamInvitationSerializer
    
    def get_queryset(self):
        """Users can see invitations they sent or received."""
        user = self.request.user
        return TeamInvitation.objects.filter(
            models.Q(inviter=user) | models.Q(invitee=user)
        )
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a team invitation."""
        invitation = self.get_object()
        user = request.user
        
        if invitation.invitee != user:
            return Response(
                {'error': 'You can only accept invitations sent to you.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if invitation.status != 'pending':
            return Response(
                {'error': 'This invitation is no longer valid.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if invitation.expires_at < timezone.now():
            invitation.status = 'expired'
            invitation.save()
            return Response(
                {'error': 'This invitation has expired.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add user to team
        team = invitation.team
        if team.has_available_slots():
            TeamMembership.objects.create(
                team=team,
                user=user,
                role='member'
            )
            invitation.status = 'accepted'
            invitation.save()
            return Response({'message': 'Successfully joined the team.'})
        else:
            return Response(
                {'error': 'Team is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        """Decline a team invitation."""
        invitation = self.get_object()
        user = request.user
        
        if invitation.invitee != user:
            return Response(
                {'error': 'You can only decline invitations sent to you.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        invitation.status = 'declined'
        invitation.save()
        return Response({'message': 'Invitation declined.'})


class TeamJoinRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing team join requests."""
    queryset = TeamJoinRequest.objects.all()
    serializer_class = TeamJoinRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TeamJoinRequestCreateSerializer
        return TeamJoinRequestSerializer
    
    def get_queryset(self):
        """Users can see requests they sent or requests for teams they lead."""
        user = self.request.user
        return TeamJoinRequest.objects.filter(
            models.Q(user=user) | models.Q(team__creator=user)
        )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a join request."""
        join_request = self.get_object()
        user = request.user
        
        if join_request.team.creator != user:
            return Response(
                {'error': 'Only team leaders can approve join requests.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if join_request.status != 'pending':
            return Response(
                {'error': 'This request has already been processed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team = join_request.team
        if team.has_available_slots():
            TeamMembership.objects.create(
                team=team,
                user=join_request.user,
                role='member'
            )
            join_request.status = 'approved'
            join_request.processed_at = timezone.now()
            join_request.save()
            return Response({'message': 'Join request approved.'})
        else:
            return Response(
                {'error': 'Team is full.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a join request."""
        join_request = self.get_object()
        user = request.user
        
        if join_request.team.creator != user:
            return Response(
                {'error': 'Only team leaders can reject join requests.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        join_request.status = 'rejected'
        join_request.processed_at = timezone.now()
        join_request.save()
        return Response({'message': 'Join request rejected.'})
