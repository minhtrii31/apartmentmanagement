from django.contrib import admin
from .models import User, Apartment, Storage, Feedback, Survey, SurveyQuestion, SurveyResponse, VehiclePass, ElectricityBill, WaterBill

# Register your models here.
admin.site.register(User)
admin.site.register(Apartment)
admin.site.register(Storage)
admin.site.register(Feedback)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyResponse)
admin.site.register(VehiclePass)
admin.site.register(ElectricityBill)
admin.site.register(WaterBill)