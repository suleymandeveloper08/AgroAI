from django.urls import path
from . import views

urlpatterns = [
    # Esasy sahypa (Surat ýüklenýän we AI analiz edilýän ýer)
    path('', views.home, name='home'),
    
    # Geçmiş sahypasy (Köne barlanan ösümlikleriň sanawy)
    path('history/', views.history, name='history'),
]