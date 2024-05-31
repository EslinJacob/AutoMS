from django import forms

from Management.models import Order


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status','additional_parts',)