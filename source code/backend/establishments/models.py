from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class Area(models.Model):
    district = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)

    unique_together = [['district', 'city']]

    def __str__(self):
        return f"{self.district}, {self.city}"
      
    class Meta:
        db_table = 'Area'
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    salary = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)

    def __str__(self):
        return self.name    
    
    class Meta:
        db_table = 'Department'

class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    address = models.CharField(max_length=200, unique=True, blank=False, null=False)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    phone_number = PhoneNumberField(unique=True, blank=False, null=False)
    car_parking_lot = models.BooleanField(default=True)
    motorbike_parking_lot = models.BooleanField(default=True)

    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
     
    class Meta:
        db_table = 'Branch'

class Table(models.Model):
    table_number = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    number_of_seats = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    status = models.CharField(
        max_length=10,
        choices = [('A', 'Available'), ('R', 'Reserved'), ('O', 'Occupied')],
        blank=False, 
        null=False, 
        default='A'
    )

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bàn số {self.table_number} của {self.branch.name}"
    
    unique_together = [['table_number', 'branch']]
    
    class Meta:
        db_table = 'Table'