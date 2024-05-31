from django.urls import path

from .views import (
    search_vehicle_model,
    search_spareparts,
)


app_name = 'search'

urlpatterns = [
    path(
        'vehiclemodel/',
        search_vehicle_model,
        name='search_vehicle_model'
    ),
    path(
        'spareparts/',
        search_spareparts,
        name='search_spareparts',
    )
]
