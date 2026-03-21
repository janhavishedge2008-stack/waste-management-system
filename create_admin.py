import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if admin already exists
if User.objects.filter(username='admin').exists():
    print("✓ Admin user already exists")
    admin = User.objects.get(username='admin')
    admin.set_password('admin123')
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print("✓ Admin password updated to: admin123")
else:
    # Create admin user
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("✓ Admin user created successfully!")
    print("  Username: admin")
    print("  Password: admin123")
