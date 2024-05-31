from django.contrib import admin

from .models import (
    VehicleModel,
    SpareParts,
)


admin.site.register(VehicleModel)
admin.site.register(SpareParts)
