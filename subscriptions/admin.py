from django.contrib import admin
from .models import Subscription, Payment, Category, PriceHistory, DeviceToken, Notification

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # J'ajoute 'user' pour que l'admin puisse voir si c'est une catégorie Global (user=None) ou Perso
    list_display = ('name', 'color', 'user')
    list_filter = ('user',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    # J'ai retiré 'status' si vous ne l'avez pas ajouté dans models.py, sinon vous pouvez le remettre
    list_display = ('name', 'user', 'price', 'currency', 'duration_unit', 'next_payment_date')
    list_filter = ('duration_unit', 'currency')
    search_fields = ('name', 'user__username') # Permet de chercher par nom d'user

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'date', 'is_paid', 'is_historical')
    list_filter = ('is_paid', 'is_historical', 'date')
    search_fields = ('subscription__name',)

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'old_price', 'apply_until')

@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')