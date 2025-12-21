from dateutil.relativedelta import relativedelta
from django.utils import timezone
from .models import Payment, Notification


def calculate_next_payment_date(subscription):
    """
    Calcule la prochaine date de paiement valide à partir d'aujourd'hui.
    """
    today = timezone.now().date()

    if subscription.start_date > today:
        return subscription.start_date

    next_date = subscription.start_date

    if subscription.duration_unit == 'days':
        delta = relativedelta(days=subscription.duration_interval)
    elif subscription.duration_unit == 'weeks':
        delta = relativedelta(weeks=subscription.duration_interval)
    elif subscription.duration_unit == 'months':
        delta = relativedelta(months=subscription.duration_interval)
    elif subscription.duration_unit == 'years':
        delta = relativedelta(years=subscription.duration_interval)
    else:
        delta = relativedelta(months=1)

    while next_date <= today:
        next_date += delta

    return next_date


def generate_payments(subscription):
    """
    Génère les paiements et crée une notification pour la prochaine échéance.
    """
    today = timezone.now().date()
    current_cycle_date = subscription.start_date

    # Définition du Delta
    if subscription.duration_unit == 'days':
        delta = relativedelta(days=subscription.duration_interval)
    elif subscription.duration_unit == 'weeks':
        delta = relativedelta(weeks=subscription.duration_interval)
    elif subscription.duration_unit == 'months':
        delta = relativedelta(months=subscription.duration_interval)
    elif subscription.duration_unit == 'years':
        delta = relativedelta(years=subscription.duration_interval)
    else:
        delta = relativedelta(months=1)

    # Sécurité : pas plus de 5 ans en arrière
    limit_date = today - relativedelta(years=5)
    if current_cycle_date < limit_date:
        while current_cycle_date < limit_date:
            current_cycle_date += delta

    payments_created = 0
    future_payment_created = False

    while not future_payment_created:
        is_past = current_cycle_date <= today

        # Gestion du prix avec historique
        amount_to_pay = subscription.price
        history = subscription.price_history.filter(apply_until__gte=current_cycle_date).order_by('apply_until').first()
        if history:
            amount_to_pay = history.old_price

        # Création du paiement
        Payment.objects.get_or_create(
            subscription=subscription,
            date=current_cycle_date,
            defaults={
                'amount': amount_to_pay,
                'is_paid': is_past,
                'is_historical': is_past
            }
        )

        if not is_past:
            # C'est le prochain paiement !
            subscription.next_payment_date = current_cycle_date
            subscription.save()
            future_payment_created = True

            # --- NOTIFICATION SUPABASE ---
            # On crée l'objet, Supabase détectera l'insertion et enverra le Realtime
            Notification.objects.create(
                user=subscription.user,
                message=f"Rappel : Prochain paiement pour {subscription.name} le {current_cycle_date}"
            )
            # -----------------------------

        current_cycle_date += delta
        payments_created += 1

        if payments_created > 1000: break

    return payments_created