from django.contrib import admin
from .models import Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'start_date', 'expiry_date')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__email')
    # Allow admins to activate subscriptions
    list_editable = ('is_active',)