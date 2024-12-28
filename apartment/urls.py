from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'apartments', views.ApartmentViewSet, basename='apartment')
router.register(r'storages', views.StorageViewSet, basename='storage')
router.register(r'feedbacks', views.FeedbackViewSet, basename='feedback')
router.register(r'surveys', views.SurveyViewSet, basename='survey')
router.register(r'survey-questions', views.SurveyQuestionViewSet, basename='survey-question')
router.register(r'survey-responses', views.SurveyResponseViewSet, basename='survey-response')
router.register(r'vehicle-passes', views.VehiclePassViewSet, basename='vehicle-pass')
router.register(r'electric-bills', views.ElectricityBillViewSet, basename='electric-bill')
router.register(r'water-bills', views.WaterBillViewSet, basename='water-bill')

urlpatterns = [
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
