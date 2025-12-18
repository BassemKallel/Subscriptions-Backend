from rest_framework import permissions,viewsets
from models import Subscription,Payment
from serializers import SubscribtionSerializer, PaymentSerializer

class SubscribtionViewSet(viewsets.ModelViewSet):
    serializers_class = SubscribtionSerializer
    permissions_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PayementViewSet(viewsets.ModelViewSet):
    serializers_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)