from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from establishments.models import Branch, Department

class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True, default=None)
    email = models.EmailField(unique=True, blank=False, null=False)
    citizen_id = models.CharField(max_length=12, unique=True, blank=True, null=True, default=None)
    full_name = models.CharField(max_length=50, blank=True, null=True, default='')
    gender = models.CharField(
        max_length=3, 
        choices=[('M', 'Male'), 
        ('F', 'Female')], 
        blank=False, 
        null=False, 
        default='M'
    )
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to= 'avatars/', blank=True, null=True, default='avatars/default.jpg')
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)
    type = models.CharField(
        max_length=8, 
        choices=[('A', 'Admin'), ('C', 'Customer'), ('E', 'Employee'), ('M', 'Manager')],
        blank=False,
        null=False,
        default='C'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    @property
    def is_staff(self):
        return self.type in ['A', 'M', 'E']

    @property
    def is_superuser(self):
        return self.type == 'A'

    def __str__(self):
        return self.full_name   
     
    class Meta:
        db_table = 'User'
    
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    resignation_date = models.DateField(default=None, blank=True, null=True)
    address = models.CharField(max_length=200, blank=False, null=False)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)
    salary = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False)

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.user.full_name 
       
    class Meta:
        db_table = 'Manager'
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    resignation_date = models.DateField(default=None, blank=True, null=True)
    address = models.CharField(max_length=200, blank=False, null=False)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        db_table = 'Employee'
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    cumulative_points = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False, default=0)
    total_points = models.IntegerField(validators=[MinValueValidator(0)], blank=False, null=False, default=0)
    tier = models.CharField(max_length=10, choices=[('M', 'Membership'), ('S', 'Silver'), ('G', 'Gold')], blank=False, null=False, default='M')
    last_tier_update = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name
    
    class Meta:
        db_table = 'Customer'

