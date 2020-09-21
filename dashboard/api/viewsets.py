from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from rest_framework.response import Response

from dashboard.models import FoodItem, MedicalRecord
from .serializers import FoodItemSerializer, MedicalRecordSerializer


class FoodItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()

class MedicalRecordViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = MedicalRecord.objects.filter(user=self.request.user).order_by("-timestamp")
        serializer = MedicalRecordSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
