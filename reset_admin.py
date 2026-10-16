
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

user = User.objects.filter(username="arij").first()

if user:
    user.set_password(os.environ["RESET_ADMIN_PASSWORD"])
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Admin password updated successfully.")
else:
    print("Admin user 'arij' was not found.")
