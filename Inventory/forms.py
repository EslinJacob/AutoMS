from django import forms

from .models import (
    VehicleModel,
    SpareParts,
)


class NewVehicleForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = (
            'model_name', 
            'brand',
            'image',
            'log',
        )


class EditVehicleForm(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = (
            'model_name', 
            'brand',
            'image',
            'log',
        )


class NewSparePartsForm(forms.ModelForm):
    class Meta:
        model = SpareParts
        fields = (
            'part_no',
            'part_name',
            'quantity',
            'cost',
            'vehicle_model',
        )


class EditSparePartsForm(forms.ModelForm):
    class Meta:
        model = SpareParts
        fields = (
            'part_no',
            'part_name',
            'quantity',
            'cost',
            'vehicle_model',
        )
