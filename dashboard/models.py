from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class FoodItem(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.TextField(blank=False)
    serving_size = models.TextField(blank=True)
    fat_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    carbohydrates_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    sugars_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    fiber_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    proteins_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    salt_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    sodium_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    alcohol_100g = models.DecimalField(max_digits=7, decimal_places=2, blank=True)

    def __str__(self):
        return self.product_name

class MedicalRecord(models.Model):
    timestamp = models.DateField(blank=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    h2_plasma_glucose = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)])
    fasting_plasma_glucose = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)])
    hbA1c = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return (self.user.username + ' - ' + str(self.timestamp))

class NutritionIntake(models.Model):
    food = models.ForeignKey(FoodItem, related_name="food_item", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    server_size = models.PositiveSmallIntegerField(default=1)
    timestamp = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return ('{username} - {food} - {date}').format(username=self.user.username, food=self.food.product_name, date=self.timestamp)
