from django.db import models
from building.models import CustomUser, Building, Utility


class Tenant(models.Model):
    """
    Defined tenant profile model for user. Profile allows users to view their assigned apartment
    object and gives control over some functionalities.
    """
    user        = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=50, null=True, blank=True)
    last_name   = models.CharField(max_length=50, null=True, blank=True)
    email       = models.EmailField(null=True, blank=True)
    phone       = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} Profile"


class Apartment(models.Model):
    """
    Defined model that represent an apartment. It takes a one to many relationship with
    the parent model (Building model) and a one to one relationship whit a user that hasn't
    admin privileges.
    """
    PAYMENT_STATUS = (
        (True, 'Paid'),
        (False, 'Unpaid')
    )

    building        = models.ForeignKey(Building, on_delete=models.CASCADE)
    tenant          = models.OneToOneField(Tenant, null=True, blank=True, on_delete=models.SET_NULL)
    surface_area    = models.IntegerField(blank=True, null=True)
    num_of_persons  = models.PositiveIntegerField(default=0)
    payment_status  = models.BooleanField(default=True, null=True, choices=PAYMENT_STATUS)
    debt            = models.FloatField(default=0)

    # define a second type of id - to avoid collision with db id if multiple buildings are created
    number_id       = models.IntegerField()

    def __str__(self):
        return f"<Apartment {self.number_id}[{self.building}]>"


class MutualUtility(models.Model):
    """
    Defines mutual utility model. Each model points to a created utility object
    with the pre defined type of 'mutual'.
    """
    apartment   = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    utility     = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)


class PowerSupply(models.Model):
    """
    Defines individual utility model. Each model points to a created utility object
    with the pre defined type of 'individual'.
    """

    STATUS = (
        (True, 'Active'),
        (False, 'Disabled')
    )

    apartment       = models.ForeignKey(Apartment, null=True, on_delete=models.CASCADE)
    utility         = models.ForeignKey(Utility, null=True, on_delete=models.CASCADE)
    index_counter   = models.IntegerField(default=0, null=True)
    status          = models.BooleanField(default=False, null=True, blank=True, choices=STATUS)

    def __str__(self):
        return f"<{self.utility.name}[Apartment {self.apartment.number_id}]>"