"""
Complete setup script - Creates database, runs migrations, loads data
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {command}")
    print()
    
    result = subprocess.run(command, shell=True, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n❌ Error: {description} failed")
        return False
    
    print(f"\n✅ {description} completed successfully")
    return True

def main():
    print("="*60)
    print("COMPLETE SETUP - Waste Management System")
    print("="*60)
    print()
    
    # Check if we're in virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not activated!")
        print("Please run: venv\\Scripts\\activate")
        print("Then run this script again.")
        sys.exit(1)
    
    print("✓ Virtual environment is active")
    print()
    
    # Step 1: Test database connection
    print("Step 1: Testing database connection...")
    result = subprocess.run([sys.executable, "test_connection.py"], capture_output=True, text=True)
    
    if "SUCCESS" not in result.stdout:
        print("\n❌ Database connection failed!")
        print("\nThe database needs to be created first.")
        print("\nPlease do ONE of the following:")
        print("\n1. Run: create_database.bat")
        print("   (This will guide you through database creation)")
        print("\n2. Or manually create in pgAdmin:")
        print("   CREATE DATABASE waste_management_db;")
        print("   CREATE USER waste_admin WITH PASSWORD 'admin123';")
        print("   GRANT ALL PRIVILEGES ON DATABASE waste_management_db TO waste_admin;")
        print("\nThen run this script again.")
        sys.exit(1)
    
    print("✅ Database connection successful!")
    
    # Step 2: Make migrations
    if not run_command(
        f"{sys.executable} manage.py makemigrations",
        "Step 2: Creating migrations"
    ):
        sys.exit(1)
    
    # Step 3: Run migrations
    if not run_command(
        f"{sys.executable} manage.py migrate",
        "Step 3: Running migrations"
    ):
        sys.exit(1)
    
    # Step 4: Load initial data
    if not run_command(
        f"{sys.executable} setup.py",
        "Step 4: Loading initial data"
    ):
        sys.exit(1)
    
    # Step 5: Create superuser
    print("\n" + "="*60)
    print("Step 5: Create superuser account")
    print("="*60)
    print("\nYou'll be asked to create an admin account.")
    print("Recommended credentials:")
    print("  Username: admin")
    print("  Email: admin@example.com")
    print("  Password: admin123")
    print()
    
    result = subprocess.run(
        f"{sys.executable} manage.py createsuperuser",
        shell=True
    )
    
    if result.returncode != 0:
        print("\n⚠️  Superuser creation skipped or failed")
        print("You can create it later with: python manage.py createsuperuser")
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\n✅ All steps completed successfully!")
    print("\nYour Waste Management System is ready to use!")
    print("\nTo start the server:")
    print("  python manage.py runserver")
    print("\nThen open your browser:")
    print("  Main Site: http://localhost:8000")
    print("  Admin Panel: http://localhost:8000/admin")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("\nFor help, see: FIX_ERRORS.md")
        sys.exit(1)
