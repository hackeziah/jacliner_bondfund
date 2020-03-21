from django.contrib import admin
from django.urls import path, reverse_lazy
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(('account.urls', 'account'), namespace="account")),
    url(r'^', include(('bond_fund.urls', 'bond_fund'), namespace="bond_fund")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
