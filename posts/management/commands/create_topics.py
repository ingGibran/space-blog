from django.core.management.base import BaseCommand
from posts.models import Topic


class Command(BaseCommand):
    help = 'Create default topics for the blog'

    def handle(self, *args, **options):
        topics = [
            "Question",
            "Chill",
            "Programming",
            "Technology",
            "University",
            "Social Life",
            "Sports",
            "General Culture",
            "Music",
            "Art",
            "Education",
            "Politics",
            "Hobby",
            "AI",
            "Work",
            "Romance",
        ]

        created_count = 0
        for topic_name in topics:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created topic: {topic_name}'))
            else:
                self.stdout.write(f'- Topic already exists: {topic_name}')

        self.stdout.write(self.style.SUCCESS(f'\nTotal topics created: {created_count}'))
        self.stdout.write(f'Total topics in database: {Topic.objects.count()}')
