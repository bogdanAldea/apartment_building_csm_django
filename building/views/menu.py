from django.shortcuts import render


def DashboardPage(request):
    return render(request, 'building/menu/admin_dashboard.html')


def SettingsPage(request):
    return render(request, 'building/menu/admin_settings.html')


def ApartmentsPage(request):
    return render(request, 'building/menu/admin_apartments.html')


def PaymentsPage(request):
    return render(request, 'building/menu/admin_payments.html')


def DocumentsPage(request):
    return render(request, 'building/menu/admin_documents.html')