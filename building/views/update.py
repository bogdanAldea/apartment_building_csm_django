from django.shortcuts import render, redirect
from building.views.menu import get_logged_user
from building.models import Utility, MainUtil
from building.forms import UpdateMainUtil


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