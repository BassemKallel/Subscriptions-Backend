from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Subscription, Category, Payment, Notification, PriceHistory
from .serializers import SubscriptionSerializer, CategorySerializer, PaymentSerializer, NotificationSerializer, PriceHistorySerializer
from .services import generate_payments
from rest_framework import permissions


# 1. ABONNEMENTS (Déjà en CRUD complet)
class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # On sauvegarde et on lance le calcul
        subscription = serializer.save(user=self.request.user)
        generate_payments(subscription)

    def perform_update(self, serializer):
        sub = serializer.save()
        sub.payments.filter(is_paid=False).delete()
        generate_payments(sub)

    @action(detail=True , methods=['post'])
    def pause(self,request):
        subscription =self.get_object()
        subscription.status = 'paused'
        subscription.save()
        return Response({'message':'Abonnement suspendu'})

    @action(detail=True, methods=['post'])
    def resume(self, request):
        subscription = self.get_object()
        subscription.status = 'active'
        subscription.save()
        return Response({'status': 'active', 'message': 'Abonnement réactivé.'})

    # Le ViewSet pour l'historique des prix
class PriceHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = PriceHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PriceHistory.objects.all()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):  # <--- CHANGÉ ICI
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(subscription__user=self.request.user).order_by('-date')

    # Optionnel : Si on crée un paiement manuellement, on l'associe à l'utilisateur via l'abonnement
    # Mais DRF gère ça assez bien si on envoie l'ID de l'abonnement.


class NotificationViewSet(viewsets.ModelViewSet):  # <--- CHANGÉ ICI
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # Important : pas besoin d'être connecté
    serializer_class = RegisterSerializer

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)