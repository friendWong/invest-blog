from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    # Expiry can be manually set by admin
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Subscription ({'Active' if self.is_active else 'Inactive'})"

# Automatically create a Subscription profile when a new User is created
@receiver(post_save, sender=User)
def create_user_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_subscription(sender, instance, **kwargs):
    instance.subscription.save()
