from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Subscription(models.Model):
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
        ('weekly', 'Hebdomadaire'),
    ]
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('cancelled', 'Annulé'),
        ('expired', 'Expiré'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='TND')
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES, default='monthly')
    start_date = models.DateField(default=timezone.now)
    next_payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Paiement de {self.amount} pour {self.subscription.name}"