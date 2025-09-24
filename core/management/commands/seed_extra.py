from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from users.models import CustomUser, UserProfile, Skill
from events.models import Event, EventCategory
from teams.models import Team, TeamMembership
import random


class Command(BaseCommand):
    help = "Seed 17 users, 5 events, and 7 teams with realistic info"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.NOTICE("Seeding data..."))

            # Ensure a few skills exist
            skill_names = [
                "Python", "Django", "JavaScript", "React", "Node.js", "UI/UX",
                "ML", "Data Science", "Docker", "Kubernetes", "PostgreSQL",
            ]
            skills = {name: Skill.objects.get_or_create(name=name)[0] for name in skill_names}

            # Create 17 users
            users = []
            for i in range(1, 18):
                email = f"user{i}@example.com"
                user, created = CustomUser.objects.get_or_create(
                    username=f"user{i}",
                    defaults={
                        "email": email,
                        "first_name": f"User{i}",
                        "last_name": "HackMate",
                    },
                )
                if created:
                    user.set_password("Password123!")
                    user.save()
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.bio = "Passionate hacker and team player."
                profile.university = random.choice(["Uni A", "Uni B", "Uni C"]) 
                profile.experience_level = random.choice(["beginner", "intermediate", "advanced"]) 
                profile.status = random.choice(["looking_for_team", "looking_for_members", "idle"]) 
                # assign 2-4 random skills
                chosen = random.sample(list(skills.values()), k=random.randint(2, 4))
                profile.save()
                profile.skills.set(chosen)
                users.append(user)

            # Ensure at least one category exists
            cat, _ = EventCategory.objects.get_or_create(name="Hackathon")

            # Create 5 events
            events = []
            for i in range(1, 6):
                ev, _ = Event.objects.get_or_create(
                    title=f"Hackathon {i}",
                    defaults={
                        "description": "A thrilling hackathon to build innovative solutions.",
                        "start_date": timezone.now() + timezone.timedelta(days=7 * i),
                        "end_date": timezone.now() + timezone.timedelta(days=7 * i + 2),
                        "location": random.choice(["Online", "Campus Hall", "Tech Park"]),
                        "organizer": random.choice(users),
                        "registration_url": "https://example.com/register",
                        "is_approved": True,
                    },
                )
                ev.categories.add(cat)
                events.append(ev)

            # Create 7 teams
            for i in range(1, 8):
                creator = random.choice(users)
                event = random.choice(events)
                team, created = Team.objects.get_or_create(
                    name=f"Team {i}",
                    event=event,
                    defaults={
                        "description": "Team focused on building an awesome project.",
                        "requirements": "Looking for Python and React devs.",
                        "interested_hackathon": event.title,
                        "creator": creator,
                        "max_members": 5,
                        "is_public": True,
                    },
                )
                if created:
                    # add creator as leader member
                    TeamMembership.objects.get_or_create(team=team, user=creator, defaults={"role": "leader"})
                    # add 2-3 more members
                    for member in random.sample(users, k=3):
                        if member != creator:
                            TeamMembership.objects.get_or_create(team=team, user=member, defaults={"role": "member"})

            self.stdout.write(self.style.SUCCESS("Seeded 17 users, 5 events, and 7 teams."))


