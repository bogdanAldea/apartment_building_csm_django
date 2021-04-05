from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .config import UtilType


def admin_dashboard(request):
    """
    Defined view function that handles the rendering of the data required by the
    dashboard.
    """

    # retrieve current logged user with admin privileges
    user = User.objects.get(username=request.user.username)

    # check if this user has an building under administration
    try:
        # retrieve the building objects assigned to currently logged user
        building = Building.objects.get(admin=user)

    except Building.DoesNotExist:
        # if there is no building assigned to this user, redirect user to a building creation form
        return redirect('building:create_residential')

    # context data to render in the template
    apartments = Apartment.objects.filter(building=building)
    occupied = apartments.filter(number_of_persons__gt=0)

    context = {
        'building': building,
        'apartments': apartments,
        'occupied': occupied,
    }

    return render(request, 'building/dashboard.html', context)


def admin_settings(request):
    """
    Defined view that renders data for the building settings page.
    """

    # retrieve currently logged user and the building he's assigned to.
    user = User.objects.get(username=request.user.username)
    building = Building.objects.get(admin=user)

    # retrieve queryset for mutual utilities
    mutual_utils = Utility.objects.filter(
        util_type=UtilType.mutual,
        building=building
    )

    # retrieve queryset for individual utility supplies
    supply_data = Utility.objects.filter(
        util_type=UtilType.individual,
        building=building
    )

    # retrieve queryset for building features
    features_data = FeatureLinked.objects.all().\
        filter(related_feature__building=building)

    # retrieve queryset for apartments that the building manages.
    apartments = Apartment.objects.all().\
        filter(building=building)

    # context data to render into the template
    context = {
        'mutual_utils': mutual_utils,
        'supply_data': supply_data.order_by('name'),
        'features_data': features_data,
        'apartments': apartments,
    }

    return render(request, 'building/settings.html', context)


def admin_counters(request):
    """
    Defined view that handles the rendering of main building counters into the counter template.
    """

    # retrieve currently logged user and the building he's assigned to
    logged_admin = User.objects.get(username=request.user.username)
    cw_building = Building.objects.get(admin=logged_admin)

    # retrieve main utilities' counters of this building.
    cold_water_main_index = cw_building.cold_water_main_index
    hot_water_main_index = cw_building.hot_water_main_index
    gas_power_main_index = cw_building.gas_power_main_index
    heating_power_main_index = cw_building.heating_power_main_index

    # context data to render into the template
    context = {
        'main_indexes': [cold_water_main_index, hot_water_main_index,
                         gas_power_main_index, heating_power_main_index],
    }

    return render(request, 'building/counters.html', context)


def admin_payments(request):
    """
    Defined view that handles the rendering of payments template.
    """
    return render(request, 'building/payments.html')


def register_page(request):
    """
    Defined view that handles new user registration with admin privileges.
    """

    # instantiate new form for user registration
    form = CreateUserForm()

    # check type of method
    if request.method == 'POST':
        # pass the request method to the form
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # redirect user to login page after registration form is submitted
            return redirect('building:login')

    # context data that renders the form into the template
    context = {'form': form}
    return render(request, 'building/register.html', context)


def login_page(request):
    """
    Defined view that handles the user login.
    """

    # check type of request method
    if request.method == "POST":
        # retrieve user's login attempt credentials
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate user with retrieved credentials
        user = authenticate(request, username=username, password=password)

        # authenticate user if exists
        if user is not None:
            login(request, user)
            # redirect authenticated user to his dashboard
            return redirect('building:dashboard')

        # if user doesn't exist, display error message
        ...

    return render(request, 'building/login.html')


def logout_user(request):
    """
    Defined view that handles user's logout.
    """
    logout(request)
    # redirects user to the login page
    return redirect('building:login')


# View for building creation when building queryset is 0.
# Redirected here form admin login is requested admin has no building under administration
def add_residential(request):
    """
    Defined View that handles residential building creation.
    When a new user with admin privileges is registered, he's redirected to a form that handles
    creation of a new custom building object.
    """
    form = CreateResidentialForm()

    if request.method == 'POST':
        form = CreateResidentialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('building:dashboard')
    context = {'form': form}
    return render(request, 'building/forms/create_residential.html', context)


# View for creating a new utility objects
def add_utility(request):
    """
    Defined view that handles creation of a new general utility. After a new utility instance is created,
    the model sends a signal which triggers the function that generates an utility instance for each existing apartment.
    """
    logged_admin = User.objects.get(username=request.user.username)
    cw_building = Building.objects.get(admin=logged_admin)

    form = CreateUtilForm()
    if request.method == 'POST':
        form = CreateUtilForm(request.POST)
        if form.is_valid():
            util = form.save(commit=False)
            util.building = cw_building
            util.save()
            return redirect('building:settings')

    context = {'form': form}
    return render(request, 'building/forms/add_utility.html', context)


def update_apartment_util_status(request, pk):
    """
    Defined view that handles the update of selected apartment's utilities
    through a formset.
    """

    # retrieve currently logged user and the building he's managing
    logged_admin = User.objects.get(username=request.user.username)
    cw_building = Building.objects.get(admin=logged_admin)

    # define a formset that takes the apartment model as the parent parameter
    # & the individual utility model as the child.
    # updates only the status bool field.
    UtilFormSet = inlineformset_factory(Apartment, IndividualUtil,
                                        fields=('status',), extra=0)

    # select apartment by accessing the primary key from data base
    apartment = Apartment.objects.get(id=pk, building=cw_building)

    # defined the form by setting the instance as selected apartment
    formset = UtilFormSet(instance=apartment)
    if request.method == 'POST':
        # pass the request method to the defined formset
        formset = UtilFormSet(request.POST, instance=apartment)
        if formset.is_valid():
            formset.save()
            # redirect user back to the settings page
            return redirect('building:settings')

    context = {'formset': formset}
    return render(request, 'building/forms/update_util_status.html', context)