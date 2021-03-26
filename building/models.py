from django.db import models
from django.contrib.auth.models import AbstractUser


# Define custom user model
class User(AbstractUser):
    is_admin    = models.BooleanField(default=True)
    is_tenant   = models.BooleanField(default=False)


# Create main parent app models
class Building(models.Model):

    admin                   = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    address                 = models.CharField(max_length=100, null=True)
    number_of_apartments    = models.IntegerField()

    hot_water_index_counter     = models.IntegerField(default=0, null=True)
    cold_water_index_counter    = models.IntegerField(default=0, null=True)
    gas_power_index_counter     = models.IntegerField(default=0, null=True)
    heating_power_index_counter = models.IntegerField(default=0, null=True)

    # taxes for independent utils
    hot_water_unit_tax      = models.FloatField(default=0, null=True)
    cold_water_unit_tax     = models.FloatField(default=0, null=True)
    gas_power_unit_tax      = models.FloatField(default=0, null=True)
    heating_power_unit_tax  = models.FloatField(default=0, null=True)

    # taxes & wages for common utils % general expenses
    sanitation_tax  = models.FloatField(default=0, null=True)
    cleaning_wages  = models.FloatField(default=0, null=True)
    maintenance     = models.FloatField(default=0, null=True)

    # features
    ...


class Features(models.Model):

    name        = models.CharField(max_length=50, null=True)
    unit_tax    = models.FloatField(default=0, null=True)
    attached_to = models.ForeignKey(Building, null=True, on_delete=models.CASCADE)