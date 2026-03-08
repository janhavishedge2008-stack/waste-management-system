"""
Setup script for Waste Management System
Run this after installing requirements.txt
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from companies.models import WasteType

def create_waste_types():
    """Create default waste types"""
    waste_types = [
        {'name': 'Plastic', 'description': 'PET, HDPE, PVC, and other plastic materials'},
        {'name': 'Paper', 'description': 'Cardboard, office paper, newspapers, magazines'},
        {'name': 'Metal', 'description': 'Aluminum cans, steel, copper, and other metals'},
        {'name': 'E-waste', 'description': 'Electronic devices, circuit boards, batteries'},
        {'name': 'Organic', 'description': 'Food waste, garden waste, compostable materials'},
        {'name': 'Glass', 'description': 'Glass bottles, jars, and containers'},
        {'name': 'Hazardous', 'description': 'Chemicals, paints, and hazardous materials'},
    ]
    
    for wt in waste_types:
        WasteType.objects.get_or_create(name=wt['name'], defaults={'description': wt['description']})
    
    print(f"✓ Created {len(waste_types)} waste types")

if __name__ == '__main__':
    print("Setting up Waste Management System...")
    create_waste_types()
    print("✓ Setup complete!")
