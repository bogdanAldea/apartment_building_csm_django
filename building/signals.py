from django.db.models.signals import post_save
from .models import Building, Apartment, User


def generate_apartments(sender, instance, created, **kwargs):
    if created:
        apartment_to_create = instance.number_of_apartments
        for number in range(1, apartment_to_create+1):
            Apartment.objects.create(
                id=number,
                building=instance
            )


post_save.connect(generate_apartments, sender=Building)

