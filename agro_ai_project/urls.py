from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ähli esasy sahypalary diagnosis app-ynyň urls.py faýlyna ugrukdyrýarys
    path('', include('diagnosis.urls')),
]

# Ýüklenen suratlary (Media) brauzerde açyp we görkezip biler ýaly şu şerti goşýarys
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)