from django.shortcuts import render, redirect
from building.forms import *
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