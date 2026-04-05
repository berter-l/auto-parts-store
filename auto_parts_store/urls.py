from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from auto_parts_store import settings

urlpatterns = [
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                  path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                  path('admin/', admin.site.urls),
                  path('blog/', include('blog.urls')),
                  path('authentication/', include('authentication.urls')),
                  path('supplier/', include('supplier.urls')),
                  path('cart/', include('cart.urls')),
                  path('parts/', include('catalog.urls')),
                  path('order/', include('orders.urls')),
                  path('', include('django_prometheus.urls'))

              ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
