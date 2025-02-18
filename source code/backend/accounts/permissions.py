from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import User, Customer, Manager, Employee

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj.id == request.user.id
        elif isinstance(obj, Customer):
            return obj.user.id == request.user.id
        elif isinstance(obj, Manager):
            return obj.user.id == request.user.id
        elif isinstance(obj, Employee):
            return obj.user.id == request.user.id
        return False

class IsSameBranchManager(BasePermission):
    def has_permission(self, request, view):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied("User is not authenticated")
            
            if request.user.type != 'M':
                raise PermissionDenied("User is not a manager")
            
            manager = Manager.objects.get(user_id=request.user.id)

            if manager.resignation_date:
                raise PermissionDenied("Manager has already resigned")
            
            if manager.branch is None:
                raise PermissionDenied("Manager does not have a valid branch assigned")
            
            request.branch = manager.branch
            return True
        
        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")
        
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Employee):
            if obj.branch != request.branch:
                raise PermissionDenied("Manager does not have permission for this object")
            return True
        return False

class IsManager(BasePermission):
    def has_permission(self, request, view):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied("User is not authenticated")
            
            if request.user.type != 'M':
                raise PermissionDenied("User is not a manager")
            
            manager = Manager.objects.get(user_id=request.user.id)

            if manager.resignation_date:
                raise PermissionDenied("Manager has already resigned")
            
            if manager.branch is None:
                raise ValueError("Manager does not have a valid branch assigned")
            
            request.branch = manager.branch
            
            return True
        
        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")
        
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Employee):
            return True
        return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated")
        
        if request.user.type != 'A':
            raise PermissionDenied("User is not an admin")
        
        return True
    
    def has_object_permission(self, request, view, obj):
        return True

class IsEmployeeOrSameBranchManager(BasePermission):
    def has_permission(self, request, view):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied("User is not authenticated")

            if request.user.type in ['A', 'C']:
                return False

            if request.user.type == 'E':
                employee = Employee.objects.get(user_id=request.user.id)

                if employee.resignation_date:
                    raise PermissionDenied("Employee has already resigned")

                request.employee = employee
                return True

            if request.user.type == 'M':
                manager = Manager.objects.get(user_id=request.user.id)

                if manager.resignation_date:
                    raise PermissionDenied("Manager has already resigned")

                if manager.branch is None:
                    raise ValueError("Manager does not have a valid branch assigned")

                request.branch = manager.branch
                request.manager = manager
                return True

        except Employee.DoesNotExist:
            raise ValueError("Employee not found")
        except Manager.DoesNotExist:
            raise ValueError("Manager not found")
        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")

        return False

    def has_object_permission(self, request, view, obj):
        try:
            if isinstance(obj, User):
                return obj.id == request.user.id

            elif isinstance(obj, Employee):
                if obj.user.id == request.user.id:
                    return True

                if request.user.type == 'M' and hasattr(request, 'branch') and obj.branch == request.branch:
                    return True

            elif isinstance(obj, Manager):
                if request.user.type == 'M' and obj.branch == request.branch:
                    return True

        except Exception as e:
            raise PermissionDenied(f"Permission check error: {str(e)}")

        return False

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated")

        if request.user.type in ['A', 'M']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            if request.user.type == 'A' or obj.id == request.user.id:
                return True
        elif isinstance(obj, Manager):
            if request.user.type == 'A' or obj.user.id == request.user.id:
                return True

        return False

