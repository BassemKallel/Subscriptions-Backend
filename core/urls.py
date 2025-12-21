from django.contrib import admin
from django.urls import path, include

# Imports pour JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('subscriptions.urls')),

    # --- ROUTES D'AUTHENTIFICATION JWT ---
    # POST /api/token/       -> Envoyer username/password, recevoir access/refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # POST /api/token/refresh/ -> Envoyer refresh token, recevoir un nouveau access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]