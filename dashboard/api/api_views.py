from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import FoodItemSerializer, NutritionIntakeSerializer, MedicalRecordSerializer
from dashboard.models import FoodItem, MedicalRecord, NutritionIntake
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

class FoodItemList(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_name','=id')

class MedicalData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        queryset = MedicalRecord.objects.filter(user=request.user).order_by('-timestamp')
        serializer = MedicalRecordSerializer(queryset, many=True)
        return Response(serializer.data)

    # def put(self, request, timestamp, format=None):
    #     try:
    #         queryset = MedicalRecord.objects.filter(user=request.user, timestamp=timestamp).order_by('-timestamp')
    #     except MedicalRecord.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     # serializer = MedicalRecordSerializer(queryset, many=True)
    #     data = {}
    #     if serializer.is_valid():
    #         serializer.save()
    #         data["success"] = "Update Successful"
    #         return Response(data=data)
    #     return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    #
    # def delete(self, request, timestamp, format=None):
    #     try:
    #         queryset = MedicalRecord.objects.filter(user=request.user, timestamp=timestamp).order_by('-timestamp')
    #     except MedicalRecord.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     operation = queryset.delete()
    #     data = {}
    #     if operation:
    #          data["success"] = "Deleted successfully"
    #     else:
    #         data["failure"] = "Delete Failed"
    #     return Response(data=data)
    #
    # def post(self, request, *args, **kwargs):
    #     pass


class NutritionIntakeData(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NutritionIntakeSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user).order_by('-timestamp')
        return queryset

class MedicalChartData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def generate_data(self, request):
        queryset = MedicalRecord.objects.filter(user=request.user).order_by('timestamp')
        data = {'labels':[], 'Fasting Plasma Glucose': [], '2-h Plasma Glucose':[], 'HbA1c': []}
        for items in queryset:
            data['labels'].append(str(items.timestamp))
            data['Fasting Plasma Glucose'].append(items.fasting_plasma_glucose)
            data['2-h Plasma Glucose'].append(items.h2_plasma_glucose)
            data['HbA1c'].append(items.hbA1c)
        return data

    def get(self, request, format=None):
        data = self.generate_data(request)
        labels = data['labels']
        default_items = [
        {
            'label': 'Fasting Plasma Glucose',
            'backgroundColor': 'rgba(0, 63, 92, 1)',
            'data': data['Fasting Plasma Glucose']
        },
        {
            'label': "2-h Plasma Glucose",
            'backgroundColor': 'rgba(188, 80, 144, 1)',
            'data': data['2-h Plasma Glucose']
        },
        {
            'label': "HbA1c",
            'backgroundColor': 'rgba(255, 166, 0, 1)',
            'data': data['HbA1c']
        }]
        data = {
            "labels": labels,
            "datasets": default_items,
        }
        return Response(data)


class NutritionIntakeChartData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def generate_data(self, request):
        queryset = NutritionIntake.objects.filter(user=request.user).order_by('-timestamp')
        # data = {'labels':[], 'productName':[],'sugar': [], 'fat':[], 'carbohydrate': [], 'protein': []}
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
        return data

    def get(self, request, format=None):
        data = self.generate_data(request)
        labels = [keys for keys in data.keys()]
        default_items = [
        {
            'label': 'Sugar',
            'backgroundColor': 'rgba(0, 63, 92, 1)',
            'data': [values['sugar'] for values in data.values()]
        },
        {
            'label': "Carbs",
            'backgroundColor': 'rgba(122, 81, 149, 1)',
            'data': [values['carbohydrates'] for values in data.values()]
        },
        {
            'label': "Fat",
            'backgroundColor': 'rgba(239, 86, 117, 1)',
            'data': [values['fat'] for values in data.values()]
        },
        {
            'label': 'protein',
            'backgroundColor': 'rgba(255, 166, 0, 1)',
            'data': [values['protein'] for values in data.values()]
        }]
        data = {
            "labels": labels,
            "datasets": default_items,
        }
        return Response(data)
