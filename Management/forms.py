from django import forms

from .models import (
    ServiceTypes,
    VehicleService,
    Customer,
    Order,
)
from core.models import EmployeeProfile


class NewServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceTypes
        fields = (
            'service_name',
            'service_etc',
            'service_cost',
            'spare_parts',
        )


class EditServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceTypes
        fields = (
            'service_name',
            'service_etc',
            'service_cost',
            'spare_parts',
        )


class NewVehicleServiceForm(forms.ModelForm):
    class Meta:
        model = VehicleService
        fields = (
            'vehicle_no',
            'model_id',
            'color',
            'manufacture_year',
            'service_types',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_no'].queryset = VehicleService.objects.filter(customer__order__status='PND')


class EditVehicleServiceServiceForm(forms.ModelForm):
    class Meta:
        model = VehicleService
        fields = (
            'vehicle_no',
            'model_id',
            'color',
            'manufacture_year',
            'service_types',
        )


class NewCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            'customer_name',
            'email',
            'phone_no',
            'vehicle_no',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_no'].queryset = VehicleService.objects.filter(
            customer__order__status__isnull=True
        )


class PlaceOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'customer',
            'engineer',
            'status',
            'additional_parts',
        )

    def __init__(self, *args, **kwargs):
        super(PlaceOrderForm, self).__init__(*args, **kwargs)
        self.fields['engineer'].queryset = EmployeeProfile.objects.filter(employee_type='mechanic')