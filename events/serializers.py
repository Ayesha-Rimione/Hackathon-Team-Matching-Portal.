from rest_framework import serializers
from .models import Event, EventParticipant, EventCategory, EventTag
from users.serializers import CustomUserSerializer


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'description', 'icon']


class EventTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTag
        fields = ['id', 'name']


class EventSerializer(serializers.ModelSerializer):
    organizer = CustomUserSerializer(read_only=True)
    tags = EventTagSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    is_registration_open = serializers.SerializerMethodField()
    is_event_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer', 'university', 'organization',
            'start_date', 'end_date', 'registration_deadline', 'max_participants',
            'is_online', 'location', 'website_url', 'registration_url',
            'rules', 'prizes', 'themes', 'is_approved', 'is_published',
            'created_at', 'updated_at', 'tags', 'participant_count',
            'is_registration_open', 'is_event_active'
        ]
        read_only_fields = ['id', 'organizer', 'created_at', 'updated_at']
    
    def get_participant_count(self, obj):
        return obj.get_participant_count()
    
    def get_is_registration_open(self, obj):
        return obj.is_registration_open()
    
    def get_is_event_active(self, obj):
        return obj.is_event_active()


class EventCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=EventTag.objects.all(),
        required=False
    )
    
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'university', 'organization',
            'start_date', 'end_date', 'registration_deadline', 'max_participants',
            'is_online', 'location', 'website_url', 'registration_url',
            'rules', 'prizes', 'themes', 'tags'
        ]
    
    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


class EventParticipantSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = EventParticipant
        fields = ['id', 'event', 'user', 'registration_date', 'status']
        read_only_fields = ['id', 'registration_date']


class EventParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipant
        fields = ['event']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, data):
        event = data['event']
        user = self.context['request'].user
        
        # Check if user is already registered
        if EventParticipant.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError("You are already registered for this event.")
        
        # Check if registration is open
        if not event.is_registration_open():
            raise serializers.ValidationError("Registration for this event is closed.")
        
        # Check if event is full
        if event.max_participants and event.get_participant_count() >= event.max_participants:
            raise serializers.ValidationError("This event is full.")
        
        return data
