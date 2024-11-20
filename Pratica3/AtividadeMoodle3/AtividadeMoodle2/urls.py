from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.http import HttpResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Teste de homepage</h1>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include('core.urls')),  
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

