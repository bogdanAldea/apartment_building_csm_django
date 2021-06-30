from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Building, Utility, MainUtil

UserModel = get_user_model()


class CreateCustomUserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = (
            'first_name', 'last_name', 'username',
            'email', 'password1', 'password2'
        )


class ResidentialRegistrationForm(ModelForm):
    class Meta:
        model = Building
        fields = (
            'street_name', 'street_number', 'city', 'county',
            'postal_code', 'apartments_capacity', 'has_elevator'
        )


class CreateUtilityForm(ModelForm):
    class Meta:
        model = Utility
        fields = '__all__'
        exclude = ('building', )


class UpdateUtilityForm(ModelForm):
    class Meta:
        model = Utility
        fields = '__all__'
        exclude = ('building', 'util_type', 'tax_type', )


class UpdateMainUtil(ModelForm):
    class Meta:
        model = MainUtil
        fields = ['index_counter']