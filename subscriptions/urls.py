from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubscriptionViewSet, CategoryViewSet, PaymentViewSet, NotificationViewSet,
    RegisterView, CurrentUserView  # <--- N'oubliez pas d'importer les nouvelles vues
)

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'categories', CategoryViewSet)
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),

    # --- AUTHENTIFICATION ---
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/me/', CurrentUserView.as_view(), name='current_user'),
]