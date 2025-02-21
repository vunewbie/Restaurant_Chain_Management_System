from .models import *

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.settings import api_settings

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['type'] = user.type
        return token

    def authenticate_user(self, identifier, password):
        try:
            user = get_user_model().objects.get(
                Q(username=identifier) |
                Q(email=identifier) |
                Q(phone_number=identifier) |
                Q(citizen_id=identifier)
            )
            
            if user.check_password(password) and user.is_active:
                return user
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        self.user = self.authenticate_user(username, password)

        if not self.user:
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')

        refresh = self.get_token(self.user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        update_last_login(None, self.user)

        return data     
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'date_created': {'read_only': True},
            'type': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs.get('password'):
            try:
                validate_password(attrs['password'])
            except ValidationError as e:
                raise serializers.ValidationError({'password': list(e.messages)})

        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        
        if password:
            user.set_password(password)
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        instance.save()
        
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation.pop('groups', None)
        representation.pop('user_permissions', None)
        
        return representation
    
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['user', 'cumulative_points', 'total_points', 'tier', 'last_tier_update']

    def validate(self, attrs):
        attrs['user']['type'] = 'C'
        
        return attrs
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        
        return customer
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['user', 'resignation_date', 'address', 'department', 'branch']

    def validate(self, attrs):
        attrs['user']['type'] = 'E'
        
        return attrs
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        employee = Employee.objects.create(user=user, **validated_data)
        
        return employee
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
    
class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ['user', 'resignation_date', 'address', 'years_of_experience', 'salary', 'branch']

    def validate(self, attrs):
        attrs['user']['type'] = 'M'
        
        return attrs
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        manager = Manager.objects.create(user=user, **validated_data)
        
        return manager
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

