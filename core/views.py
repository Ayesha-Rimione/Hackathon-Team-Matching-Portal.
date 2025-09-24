from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from users.forms import ProfileForm
from teams.forms import TeamForm
from teams.models import Team
from events.models import Event
from users.models import CustomUser


def home(request):
    """Home page view."""
    return render(request, 'core/home.html')


def about(request):
    """About page view."""
    return render(request, 'core/about.html')


@login_required
def dashboard(request):
    """User dashboard view."""
    return render(request, 'core/dashboard.html')


@login_required
def profile(request):
    """User profile view."""
    # Ensure profile exists for current user
    from users.models import UserProfile
    UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile.html')


@login_required
def edit_profile(request):
    """Edit profile view."""
    from users.models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile_edit.html', {'form': form})


def teams(request):
    """Public teams listing page."""
    teams_qs = Team.objects.select_related('creator', 'event').prefetch_related('members', 'required_skills').filter(is_public=True)
    return render(request, 'core/teams.html', { 'teams': teams_qs })


@login_required
def create_team(request):
    """Create a new team; leader becomes creator and first member."""
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user
            team.save()
            form.save_m2m()
            # add creator as member/leader
            from teams.models import TeamMembership
            TeamMembership.objects.get_or_create(team=team, user=request.user, defaults={'role': 'leader'})
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm()
    return render(request, 'core/team_create.html', {'form': form})


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    # compute membership booleans for template (avoid method calls in template)
    is_leader = request.user == team.creator
    is_member = team.members.filter(id=request.user.id).exists()

    # handle join request submission here
    if request.method == 'POST' and not is_leader and not is_member:
        from teams.models import TeamJoinRequest
        message = request.POST.get('message', '').strip()
        # only create if not already pending
        existing = TeamJoinRequest.objects.filter(team=team, user=request.user, status='pending').exists()
        if not existing:
            TeamJoinRequest.objects.create(team=team, user=request.user, message=message)
        return redirect('team_detail', pk=team.pk)

    context = {
        'team': team,
        'is_leader': is_leader,
        'is_member': is_member,
    }
    return render(request, 'core/team_detail.html', context)


@login_required
def team_requests(request, pk):
    from teams.models import TeamJoinRequest
    team = get_object_or_404(Team, pk=pk)
    requests_qs = TeamJoinRequest.objects.filter(team=team).select_related('user')
    return render(request, 'core/team_requests.html', {'team': team, 'requests': requests_qs})


@login_required
def team_request_action(request, pk, req_id, action):
    from teams.models import TeamJoinRequest, TeamMembership
    team = get_object_or_404(Team, pk=pk)
    join_req = get_object_or_404(TeamJoinRequest, pk=req_id, team=team)
    if request.user != team.creator:
        return redirect('team_requests', pk=pk)
    if action == 'accept' and join_req.status == 'pending':
        # add to members
        TeamMembership.objects.get_or_create(team=team, user=join_req.user, defaults={'role': 'member'})
        join_req.status = 'approved'
        from django.utils import timezone
        join_req.processed_at = timezone.now()
        join_req.save()
    elif action == 'reject' and join_req.status == 'pending':
        from django.utils import timezone
        join_req.status = 'rejected'
        join_req.processed_at = timezone.now()
        join_req.save()
    return redirect('team_requests', pk=pk)


def events(request):
    """Public events listing page."""
    events_qs = Event.objects.select_related('organizer').all().order_by('-start_date')
    return render(request, 'core/events.html', { 'events': events_qs })


@login_required
def messaging(request):
    """Messaging page view."""
    return render(request, 'core/messaging.html')


@login_required
def messages_inbox(request):
    from messaging.models import Message as ConversationMessage
    inbox = ConversationMessage.objects.filter(receiver=request.user).select_related('sender').order_by('-created_at')
    sent = ConversationMessage.objects.filter(sender=request.user).select_related('receiver').order_by('-created_at')
    return render(request, 'core/messages_inbox.html', {'inbox': inbox, 'sent': sent})


@login_required
def message_send(request, user_id):
    from messaging.models import Message as ConversationMessage
    receiver = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            ConversationMessage.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('messages_inbox')
    return render(request, 'core/message_send.html', {'receiver': receiver})


@csrf_exempt
def api_test(request):
    """Simple API test endpoint."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'message': 'API is working!', 'received_data': data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'message': 'HackMate API is running!'})
