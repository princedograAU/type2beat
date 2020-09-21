from  rest_framework import serializers
from dashboard.models import FoodItem, NutritionIntake, MedicalRecord
from datetime import datetime

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('id', 'product_name', 'serving_size',
                    'fat_100g', 'carbohydrates_100g', 'sugars_100g',
                    'fiber_100g', 'proteins_100g', 'salt_100g', 'sodium_100g', 'alcohol_100g')


class NutritionIntakeSerializer(serializers.ModelSerializer):
    food_item = serializers.CharField(source='food.product_name',read_only=True)
    class Meta:
        model = NutritionIntake
        fields = ('server_size', 'timestamp','food','food_item')

    def to_representation(self, instance):
        representation = super(NutritionIntakeSerializer, self).to_representation(instance)
        representation['timestamp'] = instance.timestamp.strftime("%d/%m/%Y %H:%M")
        return representation

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ('timestamp', 'h2_plasma_glucose', 'fasting_plasma_glucose', 'hbA1c')

    def to_representation(self, instance):
        representation = super(MedicalRecordSerializer, self).to_representation(instance)
        representation['timestamp'] = instance.timestamp.strftime("%d/%m/%Y")
        return representation
