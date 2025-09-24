from rest_framework import serializers
from .models import CustomUser, UserProfile, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category']


class UserProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'bio', 'university', 'organization', 'experience_level',
            'interests', 'availability', 'status', 'linkedin_url', 'github_url',
            'portfolio_url', 'avatar', 'skills', 'created_at', 'updated_at'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id', 'email']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Skill.objects.all(),
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'university', 'organization', 'experience_level',
            'interests', 'availability', 'status', 'linkedin_url', 'github_url',
            'portfolio_url', 'avatar', 'skills'
        ]


class UserSearchSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'profile']
