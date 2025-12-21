from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True , blank=True)
    color = models.CharField(max_length=7, default='#000000')

    def __str__(self):
        return self.name


class Subscription(models.Model):
    DURATION_UNIT_CHOICES = [
        ('days', 'Jours'),
        ('weeks', 'Semaines'),
        ('months', 'Mois'),
        ('years', 'Années'),
    ]
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('cancelled', 'Annulé'),
        ('expired', 'Expiré'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('TND', 'Dinar Tunisien')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='subscriptions')
    name = models.CharField(max_length=100)

    # Correction: 'price' au lieu de 'cost'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='TND')

    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES)
    duration_interval = models.PositiveIntegerField(default=1)

    start_date = models.DateField(default=timezone.now)
    # Correction typo: next_payment_date (sans 'e' après pay)
    next_payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Correction typo: created_at (sans 'e' après created)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.price} {self.currency})"


class PriceHistory(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='price_history')
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    apply_until = models.DateField()

    class Meta:
        ordering = ['-apply_until']


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    is_historical = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.subscription.name} - {self.amount} {self.subscription.currency}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notif pour {self.user.username} : {self.message}"

class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    fcm_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=10, choices=(('android', 'Android'), ('ios', 'iOS')))
    created_at = models.DateTimeField(auto_now_add=True)

