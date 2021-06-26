from django.urls import path
from .views import menu

app_name = 'building'

urlpatterns = [

    # sidebar urls
    path("", menu.DashboardPage, name="admin_dashboard"),
    path("settings/", menu.SettingsPage, name="admin_settings"),
    path("apartments/", menu.ApartmentsPage, name="admin_apartments"),
    path("payments/", menu.PaymentsPage, name="admin_payments"),
    path("documents/", menu.DocumentsPage, name="admin_documents"),
]