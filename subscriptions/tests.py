from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Category, Subscription, Payment, Notification
from datetime import date


class AdminCategoryTests(APITestCase):
    """
    Test 1: Vérifier la sécurité des Catégories (Admin vs User)
    """

    def setUp(self):
        # 1. On crée un utilisateur normal
        self.user = User.objects.create_user(username='etudiant', password='password123')

        # 2. On crée une catégorie "Globale" (Admin) directement en base
        self.global_category = Category.objects.create(name="Streaming", color="#FF0000", user=None)

        # 3. URL de l'API catégories
        self.url = reverse('category-list')  # correspond à /api/categories/

    def test_user_can_view_categories(self):
        """Un utilisateur connecté doit voir les catégories globales"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Streaming")

    def test_user_cannot_create_category(self):
        """Un utilisateur NE PEUT PAS créer de catégorie (405 Method Not Allowed)"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Hacking", "color": "#000000"}

        # On essaie de faire un POST
        response = self.client.post(self.url, data)

        # Comme on a mis ReadOnlyModelViewSet, ça doit bloquer
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class UserFlowTests(APITestCase):
    """
    Test 2: Le parcours complet de l'étudiant (Abonnement & Calculs)
    """

    def setUp(self):
        # Création User
        self.user = User.objects.create_user(username='sami', password='password123')
        self.client.force_authenticate(user=self.user)

        # Catégorie nécessaire pour l'abonnement
        self.category = Category.objects.create(name="Logiciels", user=None)

        self.sub_url = reverse('subscription-list')  # /api/subscriptions/

    def test_create_subscription_generates_payments(self):
        """Créer un abonnement doit déclencher le calcul automatique des paiements"""
        data = {
            "name": "Adobe Creative Cloud",
            "price": "30.00",
            "currency": "TND",
            "duration_unit": "months",
            "duration_interval": 1,
            "start_date": "2023-11-01",  # Date dans le passé (2 mois environ)
            "category": self.category.id
        }

        # 1. Action : POST /subscriptions/
        response = self.client.post(self.sub_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sub_id = response.data['id']

        # 2. Vérification : Est-ce que les paiements sont créés ?
        # Depuis Nov 2023 jusqu'à aujourd'hui, il devrait y avoir plusieurs paiements
        payment_count = Payment.objects.filter(subscription_id=sub_id).count()
        self.assertTrue(payment_count >= 1, "Le système aurait dû générer des paiements")

        # 3. Vérification : Est-ce qu'une notification est créée ?
        notif_count = Notification.objects.filter(user=self.user).count()
        self.assertEqual(notif_count, 1, "Une notification de bienvenue/rappel aurait dû être créée")

    def test_data_isolation(self):
        """Sami ne doit pas voir les abonnements de Ahmed"""
        # Sami crée un abonnement
        Subscription.objects.create(
            user=self.user,
            name="Sami Netflix",
            price=10,
            start_date=date(2024, 1, 1),
            category=self.category
        )

        # On change d'utilisateur (Ahmed arrive)
        ahmed = User.objects.create_user(username='ahmed', password='password123')
        self.client.force_authenticate(user=ahmed)

        # Ahmed demande la liste des abonnements
        response = self.client.get(self.sub_url)

        # La liste doit être vide pour Ahmed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_update_payment_status(self):
        """L'utilisateur peut marquer un paiement comme payé"""
        # Création manuelle d'un abonnement et d'un paiement
        sub = Subscription.objects.create(
            user=self.user, name="Spotify", price=10, start_date=date(2024, 1, 1), category=self.category
        )
        payment = Payment.objects.create(
            subscription=sub, amount=10, date=date(2024, 2, 1), is_paid=False
        )

        url = reverse('payment-detail', args=[payment.id])
        data = {"is_paid": True}

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérification en base
        payment.refresh_from_db()
        self.assertTrue(payment.is_paid)