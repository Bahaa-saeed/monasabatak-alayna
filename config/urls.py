from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("places/", views.venue_list, name="venue_list"),
    path("places/<int:pk>/", views.venue_detail, name="venue_detail"),
    path("plan/", views.request_create, name="request_create"),
    path("request/success/<str:reference>/", views.request_success, name="request_success"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
