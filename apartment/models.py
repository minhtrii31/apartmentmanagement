from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
    
class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Apartment(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='apartments')
    move_in_date = models.DateField()
    num_registered_people = models.PositiveIntegerField()
    address = models.TextField()

    class Meta:
        db_table = 'apartment'

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
    
class Storage(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
    ]
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, related_name='storages')
    item_name = models.CharField(max_length=255)
    item_image = CloudinaryField('item_image', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta: 
        db_table = 'storages'

    def __str__(self):
        return self.item_name
    
class Feedback(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, related_name='feedbacks') 
    type = models.CharField(max_length=255, default='Service')
    content = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta: 
        db_table = 'feedbacks'

    def __str__(self):
        return self.content
    
class Survey(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta: 
        db_table = 'surveys'

    def __str__(self):
        return self.title
    
class SurveyQuestion(BaseModel):
    survey = models.ForeignKey('Survey', related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()

    class Meta: 
        db_table = 'survey_questions'

    def __str__(self):
        return self.question_text
    
class SurveyResponse(BaseModel): 
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, related_name='responses') 
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='survey_responses') 
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE, related_name='responses') 
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    response_text = models.TextField(null=True, blank=True)

    class Meta: 
        db_table = 'survey_responses'

    def __str__(self):
        return f'{self.user} - {self.survey}'
    
class VehiclePass(BaseModel): 
    VEHICLE_TYPE_CHOICES = [
        ('car', 'Car'),
        ('motorbike', 'Motorbike'),
        ('bike', 'Bike'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, related_name='vehicle_passes') 
    relative_name = models.CharField(max_length=255) 
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES) 
    vehicle_name = models.CharField(max_length=255, null=True, blank=True)
    license_plate = models.CharField(max_length=50, unique=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES) 
    
    class Meta: 
        db_table = 'vehicle_passes'

    def __str__(self):
        return self.relative_name

class ElectricityBill(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, related_name='electric_bills')
    month = models.DateField()
    previous_index = models.IntegerField()
    current_index = models.IntegerField()
    total_kwh = models.IntegerField(editable=False, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    class Meta:
        db_table = 'electric_bills'

    def calculate_total_amount(self):
        rates = [
            (50, 1678),
            (50, 1734), 
            (100, 2014),
            (100, 2536),
            (100, 2834),
        ]
        remaining_kwh = self.total_kwh
        amount = 0

        for limit, rate in rates:
            if remaining_kwh <= 0:
                break
            used_kwh = min(remaining_kwh, limit)
            amount += used_kwh * rate
            remaining_kwh -= used_kwh

        if remaining_kwh > 0:
            amount += remaining_kwh * 2927

        return amount * 1.1

    def save(self, *args, **kwargs):
        if self.current_index < self.previous_index:
            raise ValueError("Current index cannot be smaller than the previous index.")
        self.total_kwh = self.current_index - self.previous_index
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

class WaterBill(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, related_name='water_bills')
    month = models.DateField()
    water_consumption = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    class Meta:
        db_table = 'water_bills'

    def calculate_total_amount(self):
        registered_people = self.apartment.num_registered_people

        if registered_people > 0:
            tiers = [
                (registered_people * 4, 6700), 
                (registered_people * 2, 12900),
            ]
            remaining_water = self.water_consumption
            amount = 0

            for limit, rate in tiers:
                if remaining_water <= 0:
                    break
                used_water = min(remaining_water, limit)
                amount += used_water * rate
                remaining_water -= used_water

            if remaining_water > 0:
                amount += remaining_water * 14400
        else:
            amount = self.water_consumption * 14400

        return amount * 1.1

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)