from django.urls import path
from .views import menu

app_name = 'apartment'

urlpatterns = [

    # sidebar urls
    path('', menu.TenantDashboardPage, name='apt_dashboard'),
]