from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')), 

] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='departments')
router.register(r'incoming', IncomingViewSet, basename='incoming')
router.register(r'dispatch', DispatchViewSet, basename='dispatch')
router.register(r'letters', LettersViewSet, basename='letters')
urlpatterns += router.urls