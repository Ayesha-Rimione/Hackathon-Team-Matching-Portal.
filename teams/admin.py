from django.contrib import admin
from .models import Team, TeamMembership, TeamInvitation, TeamJoinRequest


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1


class TeamInvitationInline(admin.TabularInline):
    model = TeamInvitation
    extra = 1


class TeamJoinRequestInline(admin.TabularInline):
    model = TeamJoinRequest
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'creator', 'get_member_count', 'max_members', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at', 'event']
    search_fields = ['name', 'description', 'creator__email', 'event__title']
    ordering = ['-created_at']
    inlines = [TeamMembershipInline, TeamInvitationInline, TeamJoinRequestInline]
    
    def get_member_count(self, obj):
        return obj.get_member_count()
    get_member_count.short_description = 'Members'


class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ['team', 'user', 'role', 'joined_at', 'is_active']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['team__name', 'user__email']
    ordering = ['-joined_at']


class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = ['team', 'inviter', 'invitee', 'status', 'created_at', 'expires_at']
    list_filter = ['status', 'created_at']
    search_fields = ['team__name', 'inviter__email', 'invitee__email']
    ordering = ['-created_at']


class TeamJoinRequestAdmin(admin.ModelAdmin):
    list_display = ['team', 'user', 'status', 'created_at', 'processed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['team__name', 'user__email']
    ordering = ['-created_at']


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMembership, TeamMembershipAdmin)
admin.site.register(TeamInvitation, TeamInvitationAdmin)
admin.site.register(TeamJoinRequest, TeamJoinRequestAdmin)
