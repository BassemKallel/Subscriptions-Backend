from django.contrib import admin
from .models import Subscription, Payment

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'currency', 'billing_cycle', 'status', 'next_payment_date')
    list_filter = ('status', 'billing_cycle')
    search_fields = ('name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'date')
    list_filter = ('date',)