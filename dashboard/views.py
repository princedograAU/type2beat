from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from .models import FoodItem, MedicalRecord, NutritionIntake
from .forms import MedicalForm
from django.views import View
from django.views.generic import TemplateView
from django.http import Http404

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# ==============================================================================
# glucose(request) -->
#  - returns glucose html page if method type is get
#  - loads user preferences about meal to databae when method type is POST
# ==============================================================================
@login_required
def glucose(request):
    # check if request type is post
    if request.method == 'POST':
        # get the fooditems selected by the user
        foodItems = request.POST['foodItems']
        # get the date and time selected by user
        timestamp = request.POST['mealTimestamp']
        timestamp = timestamp[:-3]
        from datetime import datetime   # import datetime
        from pytz import timezone       # import timezone
        timestamp = datetime.strptime(timestamp, "%m/%d/%Y %H:%M")
        # change format of datetime to timexone because it takes timezone as a time
        timestamp = timestamp.replace(tzinfo=timezone('UTC'))
        server_size = request.POST['serveSize']
        server_size = server_size.split(" ") # splitting the string
        counter=0
        for item in foodItems.split(" "):
            nutrition_intake = NutritionIntake()
            nutrition_intake.food = FoodItem.objects.get(pk=int(item))
            nutrition_intake.timestamp = timestamp
            nutrition_intake.server_size = int(server_size[counter])
            nutrition_intake.user =  request.user
            nutrition_intake.save()
            counter+=1
        messages.success(request, f'Successfully recorded your meal intake')
        return redirect('glucose')
    else:
        return render(request, 'glucose.html')

@login_required
def medical(request):
    if request.method == 'POST':
        form = MedicalForm(request.POST)
        form.instance.user = request.user
        from datetime import datetime
        queryset = MedicalRecord.objects.filter(user=request.user, timestamp__startswith=datetime.strptime(request.POST['timestamp'], "%Y-%m-%d").date())
        if queryset:
            messages.error(request, f'Record with similar date exists')
            return redirect('medical')
        else:
            if form.is_valid():
                messages.success(request, f'Successfully recorded values')
                form.save()
            else:
                if datetime.strptime(request.POST['timestamp'], "%Y-%m-%d") > datetime.today():
                    messages.error(request, f'Selected date cannot be greater than today\'s date')
                elif float(request.POST['h2_plasma_glucose']) < 0:
                    messages.error(request, f'2H Plasma Glucose Value should be positive')
                elif float(request.POST['fasting_plasma_glucose']) < 0:
                    messages.error(request, f'Fasting Plasma Glucose Value should be positive')
                elif float(request.POST['hbA1c']) < 0:
                    messages.error(request, f'HbA1c Value should be positive')
                elif float(request.POST['hbA1c']) == 0.0 and float(request.POST['fasting_plasma_glucose']) == 0.0 and float(request.POST['h2_plasma_glucose']) == 0.0:
                    messages.error(request, f'All Parameter values cannot be empty')
                else:
                    messages.success(request, f'Successfully recorded values')
                    form.save()
            return redirect('medical')
    else:
        form = MedicalForm()
        return render(request, 'medical.html', {'medicalform' : form})

@login_required
def history(request):
    return render(request, 'history.html')

class ManageRecords(TemplateView):
    template_name = 'manage.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

@login_required
def nutrition_details(request, timestamp):
    from datetime import datetime
    timestamp = datetime.strptime(timestamp, "%d/%m/%Y")
    queryset = NutritionIntake.objects.filter(user=request.user, timestamp__startswith=timestamp.strftime("%Y-%m-%d")).order_by('-timestamp')
    return render(request, 'nutrition-details.html',{'records':queryset})

@login_required
def nutrition_records(request):
    queryset = NutritionIntake.objects.filter(user=request.user).order_by('-timestamp')
    data = {}
    for result in queryset:
        if result.timestamp.strftime("%d/%m/%Y") in data:
            data[result.timestamp.strftime("%d/%m/%Y")]["carbohydrates"] += result.food.carbohydrates_100g
            data[result.timestamp.strftime("%d/%m/%Y")]["protein"] += result.food.proteins_100g
            data[result.timestamp.strftime("%d/%m/%Y")]["fat"] += result.food.fat_100g
            data[result.timestamp.strftime("%d/%m/%Y")]["sugar"] += result.food.sugars_100g
        else:
            data[result.timestamp.strftime("%d/%m/%Y")] = {"carbohydrates": result.food.carbohydrates_100g,
                                                           "protein": result.food.proteins_100g,
                                                           "fat": result.food.fat_100g,
                                                           "sugar": result.food.sugars_100g}
    return render(request, 'manage-nutrition-records.html', {'records': data})

@login_required
def delete_nutrition_all(request, timestamp):
    from datetime import datetime
    timestamp = datetime.strptime(timestamp, "%d/%m/%Y")
    queryset = NutritionIntake.objects.filter(user=request.user, timestamp__startswith=timestamp.strftime("%Y-%m-%d")).order_by('-timestamp')

    if request.method == "POST":
        messages.success(request, f'Item Deleted Successfully')
        queryset.delete()
        return redirect('nutrition_records')
    return render(request, 'delete-nutrition-all.html',{'records':queryset})

@login_required
def delete_nutrition(request, pk):
    try:
        queryset = NutritionIntake.objects.get(id=pk)
    except NutritionIntake.DoesNotExist:
        raise HTTP404('Nutrition Intake record not found')
    if request.method == "POST":
        messages.success(request, f'Item Deleted Successfully')
        queryset.delete()
        return redirect('nutrition_records')
    return render(request, 'delete-nutrition.html',{'records':queryset})

@login_required
def medical_records(request):
    data = MedicalRecord.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'manage-medical-records.html', {'records': data})

@login_required
def update_medical_record(request, pk):
    try:
        record = MedicalRecord.objects.get(id=pk)
        form = MedicalForm(instance=record)
    except MedicalRecord.DoesNotExist:
        raise HTTP404('Medical Record Not Found')

    if request.method == 'POST':
        form = MedicalForm(request.POST, instance=record)
        if form.is_valid():
            messages.success(request, f'Successfully recorded values')
            form.save()
            return redirect('manage_medical_records')

    return render(request, 'update-medical-record.html', {'form': form})

@login_required
def delete_medical_record(request, pk):
    try:
        record = MedicalRecord.objects.get(id=pk)
    except MedicalRecord.DoesNotExist:
        raise HTTP404('Medical Record Not Found')

    if request.method == 'POST':
        messages.success(request, f'Item Deleted Successfully')
        record.delete()
        return redirect('manage_medical_records')
    return render(request, 'delete-medical-record.html', {'record':record})

def HistoryView(TemplateView):
    template_name = 'history.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
