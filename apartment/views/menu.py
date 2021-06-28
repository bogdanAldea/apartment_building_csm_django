from django.shortcuts import render


def TenantDashboardPage(request):
    return render(request, 'apartment/menu/tenant_dashboard.html')


def TenantDocumentsPage(request):
    return render(request, 'apartment/menu/tenant_documents.html')