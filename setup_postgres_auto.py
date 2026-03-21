import psycopg
import sys

print("=" * 70)
print("PostgreSQL Database Setup")
print("=" * 70)

postgres_password = "root"

try:
    conn = psycopg.connect(
        dbname='postgres',
        user='postgres',
        password=postgres_password,
        host='localhost',
        port='5432',
        autocommit=True
    )
    print("✓ Connected to PostgreSQL")
    
    cursor = conn.cursor()
    
    # Check and create user
    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname='waste_admin'")
    if cursor.fetchone():
        print("✓ User waste_admin exists")
        cursor.execute("ALTER USER waste_admin WITH PASSWORD 'admin123'")
        print("✓ Password updated")
    else:
        cursor.execute("CREATE USER waste_admin WITH PASSWORD 'admin123'")
        print("✓ User waste_admin created")
    
    # Check and create database
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='waste_management_db'")
    if cursor.fetchone():
        print("✓ Database waste_management_db exists")
    else:
        cursor.execute("CREATE DATABASE waste_management_db OWNER waste_admin")
        print("✓ Database waste_management_db created")
    
    cursor.execute("GRANT ALL PRIVILEGES ON DATABASE waste_management_db TO waste_admin")
    cursor.execute("ALTER USER waste_admin CREATEDB")
    print("✓ Privileges granted")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("SUCCESS! PostgreSQL setup complete!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    sys.exit(1)
