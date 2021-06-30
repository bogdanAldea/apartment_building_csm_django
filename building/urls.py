from django.urls import path
from .views import menu, auth, create, update

app_name = 'building'

urlpatterns = [

    # sidebar urls
    path("", menu.DashboardPage, name="admin_dashboard"),
    path("settings/", menu.SettingsPage, name="admin_settings"),
    path("apartments/", menu.ApartmentsPage, name="admin_apartments"),
    path("payments/", menu.PaymentsPage, name="admin_payments"),
    path("documents/", menu.DocumentsPage, name="admin_documents"),

    # user authentication urls
    path('register/', auth.RegisterPage, name='register'),
    path('login/', auth.LoginPage, name='login'),
    path('logout/', auth.LogoutUser, name='logout'),

    # crud operations: CREATE
    path('create-residential/', create.CreateResidentialBuilding, name='create-residential'),
    path('create-utility/', create.CreateUtility, name='create_utility'),

    # crud operations: UPDATE
    path('main-utils/<int:pk>/update-index/', update.UpdateMainCounters, name='update_main_utils-index'),
    path('main-utils/<int:pk>/update-status/', update.UpdateUtilityStatus, name='update_main_utils-status'),
]