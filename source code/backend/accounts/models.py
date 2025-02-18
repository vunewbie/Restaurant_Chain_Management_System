from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from establishments.models import Branch, Department

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, 
                    phone_number=None, citizen_id=None, full_name=None, 
                    gender=None, date_of_birth=None, **extra_fields):
        
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        if not phone_number:
            raise ValueError("The Phone Number field must be set")
        if not citizen_id:
            raise ValueError("The Citizen ID field must be set")
        if not full_name:
            raise ValueError("The Full Name field must be set")
        if not gender:
            raise ValueError("The gender field must be set")
        if not date_of_birth:
            raise ValueError("The date of birth field must be set")

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, 
                          phone_number=phone_number, citizen_id=citizen_id, 
                          full_name=full_name, gender=gender, 
                          date_of_birth=date_of_birth, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, email=None, password=None, 
                         phone_number=None, citizen_id=None, full_name=None, 
                         gender=None, date_of_birth=None, **extra_fields):
        
        extra_fields.setdefault('avatar', 'avatars/admin.jpg')
        extra_fields.setdefault('type', 'A')

        return self.create_user(username, email, password, phone_number, citizen_id, full_name, gender, date_of_birth, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    phone_number = PhoneNumberField(unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    citizen_id = models.CharField(max_length=12, unique=True, blank=False, null=False)
    full_name = models.CharField(max_length=50, blank=False, null=False)
    gender = models.CharField(max_length=3, choices=[('M', 'Male'), ('F', 'Female')], blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number', 'citizen_id', 'full_name', 'gender', 'date_of_birth']

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

