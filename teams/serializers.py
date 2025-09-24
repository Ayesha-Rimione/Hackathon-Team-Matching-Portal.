from rest_framework import serializers
from .models import Team, TeamMembership, TeamInvitation, TeamJoinRequest
from users.serializers import CustomUserSerializer, SkillSerializer
from users.models import Skill


class TeamMembershipSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = TeamMembership
        fields = ['id', 'user', 'role', 'joined_at', 'is_active']


class TeamSerializer(serializers.ModelSerializer):
    creator = CustomUserSerializer(read_only=True)
    members = TeamMembershipSerializer(many=True, read_only=True)
    required_skills = SkillSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    has_available_slots = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'event', 'creator', 'members',
            'required_skills', 'max_members', 'is_public', 'created_at',
            'updated_at', 'member_count', 'has_available_slots'
        ]
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.get_member_count()
    
    def get_has_available_slots(self, obj):
        return obj.has_available_slots()


class TeamCreateSerializer(serializers.ModelSerializer):
    required_skills = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Skill.objects.all(),
        required=False
    )
    
    class Meta:
        model = Team
        fields = ['name', 'description', 'event', 'required_skills', 'max_members', 'is_public']
    
    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class TeamInvitationSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    inviter = CustomUserSerializer(read_only=True)
    invitee = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = TeamInvitation
        fields = [
            'id', 'team', 'inviter', 'invitee', 'message', 'status',
            'created_at', 'expires_at'
        ]
        read_only_fields = ['id', 'inviter', 'created_at']


class TeamInvitationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInvitation
        fields = ['team', 'invitee', 'message']
    
    def create(self, validated_data):
        validated_data['inviter'] = self.context['request'].user
        return super().create(validated_data)


class TeamJoinRequestSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = TeamJoinRequest
        fields = ['id', 'team', 'user', 'message', 'status', 'created_at', 'processed_at']
        read_only_fields = ['id', 'user', 'created_at']


class TeamJoinRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamJoinRequest
        fields = ['team', 'message']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
