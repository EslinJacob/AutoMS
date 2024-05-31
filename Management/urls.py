from django.urls import path

from .views import (
    management_home,
    new_servicetypes_form,
    all_servicetypes,
    edit_servicetypes_form,
    delete_servicetype,
    new_customer_form,
    new_vehicleservice_form,
    place_order,
    all_vehicleservice,
    checkout_order,
    checkout_fail,
)


app_name = 'management'

urlpatterns = [
    path('', management_home, name='management_home'),
    path('new_servicetypes/', new_servicetypes_form, name='new_servicetypes'),
    path('all_servicetypes/', all_servicetypes, name='all_servicetypes'),
    path('<uuid:pk>/edit_servicetypes/', edit_servicetypes_form, name='edit_servicetypes'),
    path('<uuid:pk>/delete_servicetypes/', delete_servicetype, name='delete_servicetype'),
    path('new_vehicleservice/', new_vehicleservice_form, name='new_vehicleservice'),
    path('new_customer/', new_customer_form, name='new_customer'),
    path('placeorder/', place_order, name='place_order'),
    path('all_vehicleservice/', all_vehicleservice, name='all_vehicleservice'),
    path('<uuid:pk>/checkout', checkout_order, name='checkout_order'),
    path('checkout_fail', checkout_fail, name='checkout_fail'),
]
