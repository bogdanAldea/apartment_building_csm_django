from django.shortcuts import render, redirect
from building.models import CustomUser, Building, MainUtil, Utility


def get_logged_user(request):
    logged_user = CustomUser.objects.get(username=request.user.username)
    building    = Building.objects.get(admin=logged_user)
    return logged_user, building


def DashboardPage(request):
    """
    Defined view function that handles the rendering of the data required by the
    dashboard.
    """

    # retrieve currently logged user with admin privileges
    current_user = request.user

    # check if this user has already a building under administration
    try:
        building = Building.objects.get(admin=current_user)
    except Building.DoesNotExist:
        return redirect('building:create-residential')

    # define context data to render inside the template
    apartment_list  = building.apartment_set.all()
    available_apts  = len(apartment_list) - len(apartment_list.filter(num_of_persons__gt=0))
    main_utils      = MainUtil.objects.filter(util__building=building)
    utils_are_empty = True

    for util in main_utils:
        if util.index_counter == 0:
            continue
        else:
            utils_are_empty = False
            break


    context = {
        'building': building,
        'apartment_list': apartment_list,
        'available_apts': available_apts,
        'utils_are_empty': utils_are_empty,
        'main_utils': main_utils
    }

    return render(request, 'building/menu/admin_dashboard.html', context)


def SettingsPage(request):
    """
    Defined view that renders data for the building settings page.
    """

    # retrieve building that has as admin the currently logged user
    _, current_building = get_logged_user(request)

    # retrieve queryset for mutual utilities & facilities
    mutual_utils = current_building.utility_set.filter(util_type="Mutual")

    # retrieve queryset for individual utilities & power supplies
    power_supplies = current_building.utility_set.filter(util_type='Individual')

    context = {
        "mutual_utils": mutual_utils,
        "power_supplies": power_supplies,
    }

    return render(request, 'building/menu/admin_settings.html', context)


def ApartmentsPage(request):
    """
    Defined view that renders all apartments and allows handling of tenant assignment through the template.
    """

    _, current_building = get_logged_user(request)
    context = {"building": current_building}

    return render(request, 'building/menu/admin_apartments.html', context)


def PaymentsPage(request):
    return render(request, 'building/menu/admin_payments.html')


def DocumentsPage(request):
    return render(request, 'building/menu/admin_documents.html')