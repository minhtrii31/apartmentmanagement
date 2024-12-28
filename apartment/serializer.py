from rest_framework.serializers import ModelSerializer
from .models import User, Feedback, Survey, SurveyQuestion, SurveyResponse, Storage, VehiclePass, ElectricityBill, WaterBill, Apartment

# User
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'phone', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True}, 
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class ApartmentSerializer(ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'

class StorageSerializer(ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SurveySerializer(ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

class SurveyQuestionSerializer(ModelSerializer):
    class Meta:
        model = SurveyQuestion
        fields = '__all__'

class SurveyResponseSerializer(ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = '__all__'

class VehiclePassSerializer(ModelSerializer):
    class Meta:
        model = VehiclePass
        fields = '__all__'

class ElectricityBillSerializer(ModelSerializer):
    class Meta:
        model = ElectricityBill
        fields = '__all__'

class WaterBillSerializer(ModelSerializer):
    class Meta:
        model = WaterBill
        fields = '__all__'