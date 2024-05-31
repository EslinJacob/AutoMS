from django.urls import path

from .views import (
    inventory_home,
    filtered_parts,
    all_vehicles,
    new_vehicle_form,
    edit_vehicle_form,
    all_spareparts,
    new_spareparts_form,
    edit_spareparts_form,
    delete_vehicle,
    delete_part,
)


app_name = 'inventory'

urlpatterns = [
    path('', inventory_home, name='inventory_home'),
    path('filtered_parts/<str:model>/', filtered_parts, name='filtered_parts'),
    path('all_vehicles/', all_vehicles, name='all_vehicles'),
    path('all_spareparts/', all_spareparts, name='all_spareparts'),
    path('new_vehicle/', new_vehicle_form, name='new_vehicle'),
    path('<str:pk>/edit_vehicle/', edit_vehicle_form, name='edit_vehicle'),
    path('<str:pk>/delete_vehicle/', delete_vehicle, name='delete_vehicle'),
    path('new_spareparts/', new_spareparts_form, name='new_spareparts'),
    path('<str:pk>/edit_spareparts/', edit_spareparts_form, name='edit_spareparts'),
    path('<str:pk>/delete_part/', delete_part, name='delete_part'),
]
