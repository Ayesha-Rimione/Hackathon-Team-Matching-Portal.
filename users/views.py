from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import CustomUser, UserProfile, Skill
from .serializers import (
    CustomUserSerializer, UserProfileSerializer, UserProfileUpdateSerializer,
    UserSearchSerializer, SkillSerializer
)


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user profiles."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['profile__university', 'profile__organization', 'profile__status', 'profile__availability']
    search_fields = ['first_name', 'last_name', 'email', 'profile__bio', 'profile__interests']
    ordering_fields = ['first_name', 'last_name', 'date_joined']
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search users by skills and other criteria."""
        queryset = self.get_queryset()
        
        # Filter by skills
        skills = request.query_params.getlist('skills')
        if skills:
            queryset = queryset.filter(profile__skills__name__in=skills).distinct()
        
        # Filter by experience level
        experience = request.query_params.get('experience')
        if experience:
            queryset = queryset.filter(profile__experience_level=experience)
        
        # Filter by status
        status_filter = request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(profile__status=status_filter)
        
        serializer = UserSearchSerializer(queryset, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user profiles."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer
    
    def get_queryset(self):
        """Users can only see their own profile and public profiles."""
        if self.action == 'list':
            return UserProfile.objects.filter(user__is_active=True)
        return UserProfile.objects.all()
    
    def perform_create(self, serializer):
        """Create profile for current user."""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Update profile for current user."""
        serializer.save(user=self.request.user)


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing skills."""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']
    ordering_fields = ['name', 'category']
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all skill categories."""
        categories = Skill.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))
