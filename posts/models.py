from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError

User = get_user_model()


class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Topic"
    )
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Title"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Autor"
    )
    description = models.TextField(
        verbose_name="Content"
    )
    image = models.ImageField(
        upload_to="posts_images/",
        blank=True,
        null=True,
        verbose_name="Image"
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='posts',
        blank=True,
        verbose_name="Topics"
    )
    likes = models.ManyToManyField(
        User,
        through='Like',
        related_name='liked_posts',
        verbose_name='Likes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Published"
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    @property
    def total_likes(self):
        return self.likes.count()   

    def clean(self):
        super().clean()
        if self.pk and self.topics.count() > 3:
            raise ValidationError("A post can have at most 3 topics.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Like(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes_received'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_given'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f"Like of {self.user.username} in {self.post.title}" 


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Post"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Author"
    )
    text = models.TextField(
        verbose_name="Comment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['created_at']

    def __str__(self):
        return f"Comment of {self.author.username} in {self.post.title}"
