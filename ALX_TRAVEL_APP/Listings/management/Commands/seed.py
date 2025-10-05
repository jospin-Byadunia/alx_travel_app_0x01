from django.core.management.base import BaseCommand
# import the Listing model
from Listings.models import Listing
from django.contrib.auth import get_user_model
import random

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **options):
        # Optional: clear old data
        Listing.objects.all().delete()

        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.ERROR(
                "No users found. Create some users first."))
            return

        for i in range(10):
            Listing.objects.create(
                host=random.choice(users),
                title=f"Listing {i+1}",
                description=f"Description for Listing {i+1}",
                price_per_night=random.randint(50, 500)
            )
        self.stdout.write(self.style.SUCCESS(
            "Successfully seeded 10 listings"))
