from django.contrib import admin
from .models import Event, EventParticipant, EventCategory, EventTag


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'organizer', 'start_date', 'end_date', 'is_approved',
        'is_published', 'get_participant_count', 'created_at'
    ]
    list_filter = ['is_approved', 'is_published', 'start_date', 'is_online']
    search_fields = ['title', 'description', 'organizer__email', 'university', 'organization']
    ordering = ['-start_date']
    inlines = [EventParticipantInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'organizer')
        }),
        ('Event Details', {
            'fields': ('start_date', 'end_date', 'registration_deadline', 'max_participants')
        }),
        ('Location & Settings', {
            'fields': ('is_online', 'location', 'website_url', 'registration_url')
        }),
        ('Organization', {
            'fields': ('university', 'organization')
        }),
        ('Content', {
            'fields': ('rules', 'prizes', 'themes')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_published')
        }),
    )
    
    def get_participant_count(self, obj):
        return obj.get_participant_count()
    get_participant_count.short_description = 'Participants'
    
    def get_queryset(self, request):
        """Show all events to admins."""
        return super().get_queryset(request)


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'status', 'registration_date']
    list_filter = ['status', 'registration_date']
    search_fields = ['event__title', 'user__email']
    ordering = ['-registration_date']


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name', 'description']
    ordering = ['name']


class EventTagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


admin.site.register(Event, EventAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(EventTag, EventTagAdmin)
