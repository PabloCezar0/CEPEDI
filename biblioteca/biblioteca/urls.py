from django.contrib import admin
from django.urls import  path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('', lambda request: HttpResponseRedirect('/core/livros/')), #evita a tela inicial (da erro)
]