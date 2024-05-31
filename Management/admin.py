from django.contrib import admin

from .models import (
    ServiceTypes,
    VehicleService,
    Customer,
    Order,
    Billing,
)


admin.site.register(ServiceTypes)
admin.site.register(VehicleService)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Billing)
