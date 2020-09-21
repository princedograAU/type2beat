from dashboard.api.viewsets import FoodItemViewSet, MedicalRecordViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('FoodItem', FoodItemViewSet, basename='FoodItem')
router.register('MedicalRecord', MedicalRecordViewSet, basename='MedicalRecord')
