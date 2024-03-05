from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users_api.urls')),
    path('api/recipe/', include('recipe_api.urls')),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
