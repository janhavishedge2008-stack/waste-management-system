import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'waste_management.settings')
django.setup()

from core.models import BlogPost

# Sample blog posts
blog_posts = [
    {
        'title': 'The Importance of Waste Segregation',
        'author': 'Admin',
        'content': '''Waste segregation is the foundation of effective waste management. By separating waste at the source, we can significantly improve recycling rates and reduce environmental pollution.

Key benefits of waste segregation:
- Reduces landfill waste by up to 70%
- Improves recycling efficiency
- Prevents contamination of recyclable materials
- Reduces greenhouse gas emissions
- Creates job opportunities in the recycling sector

Start segregating your waste today into these categories:
1. Organic waste (food scraps, garden waste)
2. Recyclables (paper, plastic, metal, glass)
3. Hazardous waste (batteries, chemicals, e-waste)
4. General waste (non-recyclable items)

Remember: Every small action counts towards a cleaner environment!'''
    },
    {
        'title': 'How Recycling Helps Combat Climate Change',
        'author': 'Admin',
        'content': '''Recycling plays a crucial role in fighting climate change by reducing greenhouse gas emissions and conserving natural resources.

Environmental Impact:
- Recycling one ton of paper saves 17 trees and 7,000 gallons of water
- Recycling aluminum saves 95% of the energy needed to produce new aluminum
- Plastic recycling reduces oil consumption significantly
- Glass recycling reduces air pollution by 20% and water pollution by 50%

How You Can Help:
1. Always use recycling bins
2. Clean containers before recycling
3. Learn what can and cannot be recycled in your area
4. Buy products made from recycled materials
5. Reduce single-use plastics

Together, we can make a difference in preserving our planet for future generations.'''
    },
    {
        'title': 'E-Waste Management: A Growing Challenge',
        'author': 'Admin',
        'content': '''Electronic waste (e-waste) is one of the fastest-growing waste streams globally. Proper e-waste management is essential for environmental protection and resource recovery.

Why E-Waste Matters:
- Contains valuable materials like gold, silver, and copper
- Contains hazardous substances that can harm the environment
- Growing at 3-5% annually worldwide
- Only 20% is currently recycled properly

What Qualifies as E-Waste:
- Old computers and laptops
- Mobile phones and tablets
- TVs and monitors
- Printers and scanners
- Batteries and chargers
- Small appliances

Proper Disposal:
- Never throw e-waste in regular trash
- Use certified e-waste recycling centers
- Donate working electronics
- Participate in e-waste collection drives

Schedule your e-waste pickup with us today!'''
    },
    {
        'title': 'Composting at Home: Turn Waste into Gold',
        'author': 'Admin',
        'content': '''Home composting is an excellent way to reduce organic waste while creating nutrient-rich soil for your garden.

Benefits of Composting:
- Reduces household waste by 30%
- Creates free, high-quality fertilizer
- Improves soil health and water retention
- Reduces methane emissions from landfills
- Saves money on fertilizers

What to Compost:
✓ Fruit and vegetable scraps
✓ Coffee grounds and tea bags
✓ Eggshells
✓ Yard trimmings
✓ Shredded paper and cardboard

What NOT to Compost:
✗ Meat and dairy products
✗ Oils and fats
✗ Pet waste
✗ Diseased plants

Getting Started:
1. Choose a composting method (bin, pile, or tumbler)
2. Layer green (nitrogen) and brown (carbon) materials
3. Keep it moist but not wet
4. Turn regularly for faster decomposition
5. Harvest compost in 2-3 months

Start composting today and contribute to a sustainable future!'''
    },
    {
        'title': 'Plastic Pollution: Facts and Solutions',
        'author': 'Admin',
        'content': '''Plastic pollution is one of the most pressing environmental challenges of our time. Understanding the problem is the first step toward finding solutions.

Shocking Statistics:
- 8 million tons of plastic enter oceans annually
- Only 9% of all plastic ever produced has been recycled
- Plastic takes 400-1000 years to decompose
- Over 1 million marine animals die from plastic pollution each year

Types of Plastic Waste:
1. Single-use plastics (bags, straws, bottles)
2. Microplastics (tiny particles from larger plastics)
3. Packaging materials
4. Fishing gear and nets

Solutions You Can Implement:
- Use reusable bags, bottles, and containers
- Avoid products with excessive packaging
- Choose products in glass or metal containers
- Support businesses that reduce plastic use
- Participate in beach and community cleanups

Corporate Responsibility:
Companies can request plastic waste through our platform for recycling and upcycling projects.

Together, we can reduce plastic pollution and protect our oceans!'''
    }
]

created_count = 0
for post_data in blog_posts:
    obj, created = BlogPost.objects.get_or_create(
        title=post_data['title'],
        defaults={
            'author': post_data['author'],
            'content': post_data['content']
        }
    )
    if created:
        created_count += 1
        print(f"✓ Created: {post_data['title']}")
    else:
        print(f"  Already exists: {post_data['title']}")

print(f"\n✓ Total blog posts in database: {BlogPost.objects.count()}")
print(f"✓ Newly created: {created_count}")
print("\nYou can now view blogs at: http://localhost:8000/blog/")
print("Admin can add/edit blogs at: http://localhost:8000/admin/core/blogpost/")
