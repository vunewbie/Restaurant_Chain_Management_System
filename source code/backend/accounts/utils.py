from .models import User

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date, datetime, timedelta

import json
import random

def create_otp():
    digits = "0123456789"
    otp = ''.join(random.choice(digits) for _ in range(6))
    return otp

def convert_types(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    elif hasattr(obj, 'id'):
        return obj.id
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def register_data_cache(data, otp_code):
    username = data['user']['username']
    cache_key = f"register_{username}"
    cache_data = {
        "data": data,
        "otp_code": otp_code,
        "last_sent": datetime.now().isoformat()
    }

    cache.set(cache_key, json.dumps(cache_data, default=convert_types), timeout=300)

def send_registration_otp_email(username, email, otp_code):
    subject = "Mã xác thực OTP từ nhà hàng Vunewbie"
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                color: #333;
                padding: 20px;
            }}
            .container {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: 0 auto;
            }}
            h1 {{
                color: #2c3e50;
            }}
            p {{
                font-size: 16px;
                line-height: 1.6;
            }}
            .otp-code {{
                font-size: 24px;
                font-weight: bold;
                color: #d35400;
                padding: 10px;
                background-color: #f2f2f2;
                display: inline-block;
                border-radius: 4px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Mã OTP xác thực yêu cầu đăng ký tài khoản</h1>
            <p>{username} thân mến,</p>
            <p>Mã xác thực OTP của bạn là:</p>
            <div class="otp-code">{otp_code}</div>
            <p>Mã xác thực chỉ có hiệu lực 5 phút. Vui lòng dùng nó để hoàn thành quá trình xác thực.</p>
            <p>Nếu bạn cảm thấy thông tin trên là không hữu ích, vui lòng bỏ qua email này.</p>
            <div class="footer">
                Trân trọng, <br>
                Vunewbie
            </div>
        </div>
    </body>
    </html>
    """
    from_email = settings.EMAIL_HOST_USER
    email_message = EmailMessage(
        subject=subject,
        body=html_body,
        from_email=from_email,
        to=[email]
    )
    email_message.content_subtype = "html"
    email_message.send(fail_silently=False)

def resend_registration_otp_email(username):
    cache_key = f"register_{username}"
    cache_data = cache.get(cache_key)

    if not cache_data:
        return ValueError("OTP code has expired or not found")
    
    cache_data = json.loads(cache_data)
    last_sent = datetime.fromisoformat(cache_data['last_sent'])

    if datetime.now() - last_sent < timedelta(minutes=1):
        raise ValueError("Please wait for 1 minute before resending OTP code")
    
    cache.delete(cache_key)
    
    new_otp_code = create_otp()

    cache_data['otp_code'] = new_otp_code
    cache_data['last_sent'] = datetime.now().isoformat()

    cache.set(cache_key, json.dumps(cache_data, default=convert_types), timeout=300)

    email = cache_data['data']['user']['email']
    send_registration_otp_email(username, email, new_otp_code)

def forgot_password_data_cache(username, otp_code):
    cache_key = f"forgot_password_{username}"
    cache_data = {
        "otp_code": otp_code,
        "last_sent": datetime.now().isoformat()
    }

    cache.set(cache_key, json.dumps(cache_data, default=convert_types), timeout=300)

def send_forgot_password_otp_email(username, email, otp_code):
    subject = "Mã xác thực OTP từ nhà hàng Vunewbie"
    html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                color: #333;
                padding: 20px;
            }}
            .container {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
                max-width: 600px;
                margin: 0 auto;
            }}
            h1 {{
                color: #2c3e50;
            }}
            p {{
                font-size: 16px;
                line-height: 1.6;
            }}
            .otp-code {{
                font-size: 24px;
                font-weight: bold;
                color: #d35400;
                padding: 10px;
                background-color: #f2f2f2;
                display: inline-block;
                border-radius: 4px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Mã OTP xác thực yêu cầu đổi mật khẩu</h1>
            <p>{username} thân mến,</p>
            <p>Mã xác thực OTP của bạn là:</p>
            <div class="otp-code">{otp_code}</div>
            <p>Mã xác thực chỉ có hiệu lực 5 phút. Vui lòng dùng nó để hoàn thành quá trình xác thực.</p>
            <p>Nếu bạn cảm thấy thông tin trên là không hữu ích, vui lòng bỏ qua email này.</p>
            <div class="footer">
                Trân trọng, <br>
                Vunewbie
            </div>
        </div>
    </body>
    </html>
    """
    from_email = settings.EMAIL_HOST_USER
    email_message = EmailMessage(
        subject=subject,
        body=html_body,
        from_email=from_email,
        to=[email]
    )
    email_message.content_subtype = "html"
    email_message.send(fail_silently=False)

def resend_forgot_password_otp_email(username):
    cache_key = f"forgot_password_{username}"
    cache_data = cache.get(cache_key)
    print(cache_data)

    if not cache_data:
        return ValueError("OTP code has expired or not found")
    
    cache_data = json.loads(cache_data)
    last_sent = datetime.fromisoformat(cache_data['last_sent'])

    if datetime.now() - last_sent < timedelta(minutes=1):
        raise ValueError("Please wait for 1 minute before resending OTP code")
    
    cache.delete(cache_key)
    
    new_otp_code = create_otp()

    cache_data['otp_code'] = new_otp_code
    cache_data['last_sent'] = datetime.now().isoformat()

    cache.set(cache_key, json.dumps(cache_data, default=convert_types), timeout=300)

    user = User.objects.get(username=username)
    send_forgot_password_otp_email(username, user.email, new_otp_code)


