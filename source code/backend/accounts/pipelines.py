from .models import User

def create_customer_profile(backend, user, response, *args, **kwargs):
    if kwargs.get('is_new'):
        user.username = response.get('email', response.get('sub'))
        user.full_name = response.get('name', user.full_name or 'Unknown User')
        user.phone_number = response.get('phone_number') or None
        user.citizen_id = None  # Nếu không có giá trị từ OAuth
        user.gender = response.get('gender', 'M')
        user.date_of_birth = None  # Nếu không có giá trị từ OAuth
        user.save()

