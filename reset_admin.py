
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = "arij"
password = os.environ.get("RESET_ADMIN_PASSWORD")

if not password:
    raise RuntimeError("RESET_ADMIN_PASSWORD is not configured.")

user, created = User.objects.get_or_create(username=username)
user.set_password(password)
user.is_active = True
user.is_staff = True
user.is_superuser = True
user.save()

print(f"Admin account {'created' if created else 'updated'} successfully.")
print(f"Username: {username}")
