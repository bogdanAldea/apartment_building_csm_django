from django.shortcuts import render, redirect
from building.forms import *
from building.views.menu import get_logged_user
from django.contrib.auth.decorators import login_required


@login_required(login_url='building:login')
def CreateResidentialBuilding(request):
    """
    Defined View that handles residential building creation.
    When a new user with admin privileges is registered, he's redirected to a form that handles
    creation of a new custom building object.
    """

    form = ResidentialRegistrationForm()
    if request.method == 'POST':
        form = ResidentialRegistrationForm(request.POST)
        if form.is_valid():
            new_residential = form.save(commit=False)
            new_residential.admin = request.user
            new_residential.save()
            return redirect('building:admin_dashboard')

    context = {'form': form}
    return render(request, 'building/forms/register_residential_building.html', context)


def CreateUtility(request):
    """
    Defined view that handles creation of a new general utility. After a new utility instance is created,
    the model sends a signal which triggers the function that generates an utility instance for each existing apartment.
    """

    _, current_building = get_logged_user(request)
    form = CreateUtilityForm()
    if request.method == 'POST':
        form = CreateUtilityForm(request.POST)
        if form.is_valid():
            new_utility = form.save(commit=False)
            # assign the newly created util to current working building
            new_utility.building = current_building
            new_utility.save()
            return redirect('building:admin_settings')

    context = {'form': form}
    return render(request, 'building/forms/create_utility.html', context)