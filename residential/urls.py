from django.urls import path
from residential import views


app_name = 'residential'

urlpatterns = [

    # sidebar menu urls
    path('', views.DashboardPage, name='dashboard'),
    path('settings/', views.SettingsPage, name='residential-settings'),

    # user/admin registration urls
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),

    # crud operations
    path('create-residential/', views.CreateResidential, name='create_residential'),
    path('create-utility/', views.CreateUtility, name='create_utility'),

    path('utility/apartment-<int:pk>/status-update/', views.UpdateUtilStatus, name='update_status'),
    path('utility/<int:pk>/update/', views.UpdateUtilityGeneral, name='update-utility'),
]