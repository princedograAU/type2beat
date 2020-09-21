from django.contrib import admin
from .models import FoodItem,MedicalRecord, NutritionIntake

# register the FoodItem model
admin.site.register(FoodItem)
admin.site.register(MedicalRecord)
admin.site.register(NutritionIntake)
