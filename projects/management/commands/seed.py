# projects/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from projects.models import Project, Pledge
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = "Seed Users, Projects, and Pledges with fake data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # -------- Users --------
        users = []
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password'
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users"))

        # -------- Projects --------
        projects = []
        for _ in range(5):
            project = Project.objects.create(
                owner=random.choice(users),
                title=fake.sentence(),
                description=fake.paragraph(),
                goal=fake.random_int(min=1000, max=10000),
                image=fake.image_url(),
                is_open=True
            )
            projects.append(project)
        self.stdout.write(self.style.SUCCESS(f"Created {len(projects)} projects"))

        # -------- Pledges --------
        pledges_count = 0
        for _ in range(10):  # total number of pledges
            project= random.choice(projects)  # random project
            supporter= random.choice(users)   # random user
            Pledge.objects.create(
                project=project,        # ✅ assign object
                supporter=supporter,  # ✅ assign object
                amount=fake.random_int(min=10, max=500),
                anonymous=fake.boolean(chance_of_getting_true=30)  # 30% chance
            )
            pledges_count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {pledges_count} pledges"))
        self.stdout.write(self.style.SUCCESS("Seeding complete!"))