from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from dashboard.models import FoodItem

class Command(BaseCommand):
    # show this when user types help
    help = "Loads data from openfoodfacts_clean.csv into our FoodItem model"

    def handle(self, *args, **options):
        counter = 0
        if FoodItem.objects.exists():
            print("Food Item data already loaded...existing")
            return
        print("Loading food item data...")
        for row in DictReader(open('dashboard/management/data_files/food_data.csv')):
            counter = counter + 1
            food = FoodItem()
            food.product_name = row['product_name']
            if food.product_name == "":
                continue
            food.serving_size = row['serving_size']
            food.fat_100g = round(float(row['fat_100g']),2)
            food.carbohydrates_100g = round(float(row['carbohydrates_100g']),2)
            food.sugars_100g = round(float(row['sugars_100g']),2)
            food.fiber_100g = round(float(row['fiber_100g']),2)
            food.proteins_100g = round(float(row['proteins_100g']),2)
            food.salt_100g = round(float(row['salt_100g']),2)
            food.sodium_100g = round(float(row['sodium_100g']),2)
            food.alcohol_100g = round(float(row['alcohol_100g']),2)
            # print(f'loading row... {counter}')
            food.save()
            self.stdout.write(f'loaded row... {counter}')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data to database'))
