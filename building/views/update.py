from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from building.views.menu import get_logged_user
from building.models import Utility, MainUtil
from building.forms import UpdateMainUtil
from apartment.models import Apartment, PowerSupply


def UpdateMainCounters(request, pk):
    _, current_building = get_logged_user(request)
    utility = MainUtil.objects.get(util__building=current_building, id=pk)
    counters = MainUtil.objects.filter(util__building=current_building)

    form = UpdateMainUtil(instance=utility)
    if request.method == 'POST':
        form = UpdateMainUtil(request.POST, instance=utility)
        if form.is_valid():
            form.save()
            return redirect('building:admin_settings')

    context = {
        "form": form,
        'utility': utility,
        'counters': counters
    }

    return render(request, 'building/forms/update_main_utils_counters.html', context)


def UpdateUtilityStatus(request, pk):
    """
    Defined view that handles the update of selected apartment's utility status
    through a formset.
    """

    # retrieve currently logged user and the building he's managing
    _, current_building = get_logged_user(request)

    # defined the formset that takes the apartment model as the parent argument
    # and the individual utility model as the child argument
    UtilStatusFormset = inlineformset_factory(
        parent_model=Apartment, model=PowerSupply, fields=('status', ), extra=0
    )

    # select apartment by accessing its primary key
    apartment = current_building.apartment_set.get(id=pk)

    # define formset by passing the queried apartment object
    formset = UtilStatusFormset(instance=apartment)
    if request.method == 'POST':
        formset = UtilStatusFormset(request.POST, instance=apartment)
        if formset.is_valid():
            formset.save()
            return redirect('building:admin_settings')

    # define context data to render into the template
    supply_name = ['Cold Water', 'Hot Water', 'Gas Power', 'Heating Power']
    form_data = zip(supply_name, formset)
    context = {
        'apartment': apartment,
        'form_data': form_data,
        'formset': formset
    }

    return render(request, 'building/forms/update_supply_status.html', context)
