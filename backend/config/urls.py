from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/favorites/', include('favorites.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/community/', include('community.urls')),
    path('api/exchanges/', include('exchanges.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/maps/', include('maps.urls')),
    path('api/videos/', include('videos.urls')),
    path('api/assets/', include('assets.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)