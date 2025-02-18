from .serializers import *
from .models import *
from .authentications import *
from .utils import *
from .permissions import *

from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.utils import timezone

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = create_otp()
            username = data['user']['username']
            email = data['user']['email']

            register_data_cache(data, otp_code)
            send_registration_otp_email(username, email, otp_code)
            
            response = {
                "message": "OTP has been sent to your email", 
                "username": username
            }
            
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsOwner]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, pk):
        customer = self.get_object()
        serializer = self.serializer_class(customer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        customer = self.get_object()
        
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Customer information has been updated successfully",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)
        
class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsManager]
    authentication_classes = [CustomTokenAuthentication]

    def get_queryset(self):
        branch = getattr(self.request, 'branch', None)
        
        if branch is None:
            return Employee.objects.none()
        
        return Employee.objects.filter(branch=branch)
    
    def get(self, request):
        employees = self.get_queryset()
        serializer = self.serializer_class(employees, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()

        if hasattr(request, 'branch'):
            data['branch'] = request.branch.id

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = create_otp()
            username = data['user']['username']
            email = data['user']['email']
            
            register_data_cache(data, otp_code)
            send_registration_otp_email(username, email, otp_code)

            response = {
                "message": "OTP has been sent to your email",
                "username": username
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsEmployeeOrSameBranchManager]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, pk):
        employee = self.get_object()
        serializer = self.serializer_class(employee)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request, pk):
        employee = self.get_object()

        if request.user.type == 'E':
            allowed_user_fields = [
                'username', 'phone_number', 'email', 'citizen_id', 
                'full_name', 'gender', 'date_of_birth', 'avatar'
            ]
            allowed_employee_fields = ['address']

        elif request.user.type == 'M':
            allowed_user_fields = []
            allowed_employee_fields = ['department']

        else:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        user_data = {}
        employee_data = {}

        for key, value in request.data.items():
            if key.startswith("user."):
                user_field = key.split(".", 1)[1]
                user_data[user_field] = value
            else:
                employee_data[key] = value

        user_data = {key: value for key, value in user_data.items() if key in allowed_user_fields}
        employee_data = {key: value for key, value in employee_data.items() if key in allowed_employee_fields}

        serializer = self.get_serializer(employee, data={'user': user_data, **employee_data}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Employee information has been successfully updated.",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)
        
    def delete(self, request, pk):
        if request.user.type != 'M':
            return Response({"detail": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        employee = self.get_object()
        user = employee.user

        user.is_active = False
        user.save()
        employee.resignation_date = timezone.now()
        employee.save()

        return Response({"message": "Employee has been resigned successfully."}, status=status.HTTP_200_OK)
    
class ManagerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsAdmin]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request):
        managers = self.get_queryset()
        serializer = self.serializer_class(managers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = create_otp()
            
            register_data_cache(data, otp_code)
            
            username = data['user']['username']
            email = data['user']['email']
            
            send_registration_otp_email(username, email, otp_code)
            
            response = {
                "message": "OTP has been sent to your email",
                "username": username
            }

            return Response(response, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
class ManagerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsManagerOrAdmin]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, pk):
        manager = self.get_object()
        serializer = self.serializer_class(manager)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        manager = self.get_object()

        if request.user.type == 'M':
            allowed_user_fields = [
                'username', 'phone_number', 'email', 'citizen_id', 
                'full_name', 'gender', 'date_of_birth', 'avatar'
            ]
            allowed_manager_fields = ['address', 'years_of_experience']
        elif request.user.type == 'A':
            allowed_user_fields = []
            allowed_manager_fields = ['branch', 'salary']
        else:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        user_data = {}
        manager_data = {}

        for key, value in request.data.items():
            if key.startswith("user."):
                user_field = key.split(".", 1)[1]
                user_data[user_field] = value
            else:
                manager_data[key] = value

        user_data = {key: value for key, value in user_data.items() if key in allowed_user_fields}
        manager_data = {key: value for key, value in manager_data.items() if key in allowed_manager_fields}

        serializer = self.get_serializer(manager, data={'user': user_data, **manager_data}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Manager information has been successfully updated.",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if request.user.type != "A":
            return Response({"detail": "You are not authorized to perform this action"}, status=status.HTTP_403_FORBIDDEN)
        
        manager = self.get_object()
        user = manager.user

        user.is_active = False
        user.save()
        
        manager.resignation_date = timezone.now()
        manager.save()

        return Response({"message": "Manager has been resigned"}, status=status.HTTP_200_OK) 

class RegisterVerifyOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp_code')
        cache_key = f"register_{username}"
        cache_data = cache.get(cache_key)
        
        if cache_data:
            cache_data = json.loads(cache_data)
            if cache_data['otp_code'] == otp_code:
                data = cache_data['data']
                user = User.objects.create_user(**data['user'])
                
                if data['user']['type'] == 'C':
                    customer = Customer.objects.create(user=user)
                elif data['user']['type'] == 'M':
                    branch = Branch.objects.get(id=data['branch'])
                    manager = Manager.objects.create(user=user, address=data['address'], years_of_experience=data['years_of_experience'], salary=data['salary'], branch=branch)
                elif data['user']['type'] == 'E':
                    department = Department.objects.get(id=data['department'])
                    branch = Branch.objects.get(id=data['branch'])
                    employee = Employee.objects.create(user=user, address=data['address'], department=department, branch=branch)
                
                cache.delete(cache_key)
                
                return Response({"message": "Account has been created"}, status=status.HTTP_201_CREATED)
            return Response({"detail": "Invalid OTP code"}, status=status.HTTP_400_BAD_REQUEST)
        
class ResendRegisterOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            username = request.data.get('username')

            if not username:
                return Response({"detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            resend_registration_otp_email(username)

            return Response({"message": "OTP has been sent to your email"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": "An error occurred"}, status=status.HTTP_400_BAD_REQUEST)
        
class ForgotPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username_or_email = request.data.get('username_or_email')

        if not username_or_email:
            return Response({"detail": "Username or email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()

        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_code = create_otp()

        forgot_password_data_cache(user.username, otp_code)

        send_forgot_password_otp_email(user.username, user.email, otp_code)

        response = {        
            "message": "OTP has been sent to your email",
            "username": user.username
        }

        return Response(response, status=status.HTTP_200_OK)
    
class ForgotPasswordVerifyOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp_code')

        cache_key = f"forgot_password_{username}"
        cache_data = cache.get(cache_key)

        if cache_data:
            cache_data = json.loads(cache_data)
            if cache_data['otp_code'] == otp_code:
                cache.delete(cache_key)
                
                user = User.objects.filter(username=username).first()
                
                if not user:
                    return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
                
                reset_token = RefreshToken.for_user(user).access_token
                response = {
                    "message": "OTP code is correct",
                    "reset_token": str(reset_token)
                }
                
                return Response(response, status=status.HTTP_200_OK)
            
            return Response({"detail": "Invalid OTP code"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "OTP code has expired or not found"}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not request.user or not hasattr(request.user, 'id'):
            return Response({"detail": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.id

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({"detail": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset successfully"}, status=status.HTTP_200_OK)
    
class ResendForgotPasswordOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            username = request.data.get('username')

            if not username:
                return Response({"detail": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(username=username).first()
            
            if not user:
                return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            resend_forgot_password_otp_email(username)

            return Response({"detail": "OTP has been sent to your email"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({"detail": "Old password and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        if old_password == new_password:
            return Response({"detail": "New password must be different from old password"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()

        return Response({"detail": "Password has been changed successfully"}, status=status.HTTP_200_OK)
        
class LogOutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

            except TokenError as e:
                return Response({"detail": f"Error while logging out: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        



