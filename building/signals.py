from django.db.models.signals import post_save
from .models import Building, Apartment, Utility, IndividualUtil, MutualUtil
from .config import UtilType


def generate_apartments(sender, instance, created, **kwargs):
    """
    Signal listens for a new building instance being created.
    When new instance was created, the signal triggers function and creates a given number of apartments
    that was set with the building instance.
    """

    # if the instance is a brand new objects and not an existing objects being updated
    if created:

        # default utils used independently by each apartment in the building.
        utils_to_create = [
            Utility(name='Cold water', provider='City', building=instance, util_type=UtilType.individual),
            Utility(name='Hot water', provider='City', building=instance, util_type=UtilType.individual),
            Utility(name='Gas power', provider='City', building=instance, util_type=UtilType.individual),
            Utility(name='Heating power', provider='City', building=instance, util_type=UtilType.individual)
        ]
        Utility.objects.bulk_create(utils_to_create)

        # number of apartments set by the building instance when created
        apartment_to_create = instance.number_of_apartments

        # list of utility objects created above filtered by the instance of the sender(newly created object)
        utilities = Utility.objects.filter(building=instance)

        # create new apartment objects
        for number in range(1, apartment_to_create+1):
            apartment = Apartment.objects.create(
                id=number,
                building=instance
            )

            # for each apartment created, add a individual utility
            for util in utilities:
                IndividualUtil.objects.create(
                    apartment=apartment,
                    individual_util=util
                )


# trigger action
post_save.connect(generate_apartments, sender=Building)


def generate_utils(sender, instance, created, **kwargs):
    """
    Signal listens for a new Utility instance being created
    and triggers creation of a new utility for each apartment.
    """

    if created:
        building = instance.building
        apartments = Apartment.objects.filter(building=building)
        for apartment in apartments:
            MutualUtil.objects.create(
                apartment=apartment,
                common_util=instance
            )


# trigger action
post_save.connect(generate_utils, sender=Utility)