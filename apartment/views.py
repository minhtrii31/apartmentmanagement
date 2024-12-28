from django.shortcuts import render

from apartment.models import User, Apartment, Storage, Feedback, Survey, SurveyQuestion, SurveyResponse, VehiclePass, ElectricityBill, WaterBill
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apartment.serializer import UserSerializer, ApartmentSerializer, StorageSerializer, FeedbackSerializer, SurveySerializer, SurveyQuestionSerializer, SurveyResponseSerializer, VehiclePassSerializer, ElectricityBillSerializer, WaterBillSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update', 'update_profile', 'check_profile_status']:
            return [permissions.IsAuthenticated()]
        if self.action == 'create_user_by_admin':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def create_user_by_admin(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    permission_classes = [IsAuthenticated]

class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    permission_classes = [IsAuthenticated]

class VehiclePassViewSet(viewsets.ModelViewSet):
    queryset = VehiclePass.objects.all()
    serializer_class = VehiclePassSerializer
    permission_classes = [IsAuthenticated]

class ElectricityBillViewSet(viewsets.ModelViewSet):
    queryset = ElectricityBill.objects.all()
    serializer_class = ElectricityBillSerializer
    permission_classes = [IsAuthenticated]

class WaterBillViewSet(viewsets.ModelViewSet):
    queryset = WaterBill.objects.all()
    serializer_class = WaterBillSerializer
    permission_classes = [IsAuthenticated]