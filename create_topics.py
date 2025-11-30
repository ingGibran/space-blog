"""
Script to create default topics for the blog.
Run with: python manage.py shell < create_topics.py
Or copy and paste into: python manage.py shell
"""

from posts.models import Topic

# List of default topics
DEFAULT_TOPICS = [
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

def create_default_topics():
    """Create default topics if they don't exist."""
    created_count = 0
    existing_count = 0
    
    for topic_name in DEFAULT_TOPICS:
        topic, created = Topic.objects.get_or_create(name=topic_name)
        if created:
            created_count += 1
            print(f"✓ Created topic: {topic_name}")
        else:
            existing_count += 1
            print(f"- Topic already exists: {topic_name}")
    
    print(f"\nSummary:")
    print(f"Created: {created_count} topics")
    print(f"Already existed: {existing_count} topics")
    print(f"Total topics in database: {Topic.objects.count()}")

if __name__ == "__main__":
    create_default_topics()
