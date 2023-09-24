
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from .api_list import api_list_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import MyTokenObtainPairView
from .swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-docs/', schema_view.with_ui('swagger',
         cache_timeout=0), name='api-docs'),

    #App urls
    path('api/accounts/', include('accounts.urls')),
    path('api/station/', include('filling_station.urls')),
    path('api/review/', include('review.urls')),
]
