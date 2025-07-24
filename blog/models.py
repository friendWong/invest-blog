from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


# -----------------------------------------------------------------------------
# Model for post categories
# -----------------------------------------------------------------------------
class Category(models.Model):
    """
    Represents a category that a blog post can belong to.
    """
    name = models.CharField(max_length=100, unique=True, help_text="The name of the category.")
    slug = models.SlugField(max_length=100, unique=True, help_text="A URL-friendly version of the name.")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------------------------------------------------------------
# The core model for a blog post
# -----------------------------------------------------------------------------
class Post(models.Model):
    """
    Represents a single blog post in the investment blog.
    The author and category fields are optional.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="A unique URL-friendly version of the title.")

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='blog_posts',
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # --- THIS FIELD WAS MISSING ---
    # It has now been restored.
    main_image = models.ImageField(
        upload_to='post_images/',
        help_text="The primary image for the post, displayed in carousels and headers."
    )
    # -----------------------------

    body = RichTextField(help_text="The main content of the post, with rich text editing.")

    tradingview_symbol = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Optional. The TradingView symbol for embedding a chart (e.g., NASDAQ:AAPL)."
    )

    tags = TaggableManager(blank=True, help_text="A comma-separated list of tags.")

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


# -----------------------------------------------------------------------------
# Models for Comments and Likes (remain unchanged)
# -----------------------------------------------------------------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.author.username} on "{self.post.title}"'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.username} likes "{self.post.title}"'