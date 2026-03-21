from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal


@receiver(pre_save, sender='pickups.PickupRequest')
def update_collected_waste_on_completion(sender, instance, **kwargs):
    """When a pickup is marked completed, add its quantity to the inventory."""
    if not instance.pk:
        return  # new object, skip

    from pickups.models import PickupRequest
    from companies.models import CollectedWaste

    try:
        old = PickupRequest.objects.get(pk=instance.pk)
    except PickupRequest.DoesNotExist:
        return

    # Only trigger when status changes TO completed
    if old.status != 'completed' and instance.status == 'completed':
        # Parse quantity estimate — default to 10kg if not parseable
        qty = Decimal('10.00')
        if instance.quantity_estimate:
            import re
            nums = re.findall(r'[\d.]+', instance.quantity_estimate)
            if nums:
                try:
                    qty = Decimal(nums[0])
                except Exception:
                    pass

        inventory, _ = CollectedWaste.objects.get_or_create(
            waste_type=instance.waste_type,
            defaults={'unit': 'kg', 'total_quantity': 0, 'available_quantity': 0}
        )
        inventory.total_quantity += qty
        inventory.available_quantity += qty
        inventory.save()

    # When status changes FROM completed (e.g. re-opened), subtract back
    elif old.status == 'completed' and instance.status != 'completed':
        from companies.models import CollectedWaste
        qty = Decimal('10.00')
        if instance.quantity_estimate:
            import re
            nums = re.findall(r'[\d.]+', instance.quantity_estimate)
            if nums:
                try:
                    qty = Decimal(nums[0])
                except Exception:
                    pass
        try:
            inventory = CollectedWaste.objects.get(waste_type=instance.waste_type)
            inventory.total_quantity = max(Decimal('0'), inventory.total_quantity - qty)
            inventory.available_quantity = max(Decimal('0'), inventory.available_quantity - qty)
            inventory.save()
        except CollectedWaste.DoesNotExist:
            pass
