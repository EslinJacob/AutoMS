from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from core.utils import check_employee_type
from core.models import EmployeeProfile
from Inventory.models import (
    VehicleModel,
    SpareParts,
)


INVE_TYPE_LIST = ['inventory', 'inve']


@login_required
def search_vehicle_model(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, INVE_TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    query = request.GET.get('query', '')
    if query:
        results = VehicleModel.objects.filter(
            Q(model_name__icontains=query) | Q(brand__icontains=query)
        )
        return render(
            request,
            'search/search_vehiclemodel.html',
            {'results': results,}
        )
    return render(
        request,
        'search/search_vehiclemodel.html',
        {'query': query}
    )


@login_required
def search_spareparts(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, INVE_TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    query = request.GET.get('query', '')
    if query:
        results = SpareParts.objects.filter(
            Q(part_no__icontains=query) | Q(part_name__icontains=query)
        )
        return render(
            request,
            'search/search_spareparts.html',
            {'results': results,}
        )
    return render(
        request,
        'search/search_spareparts.html',
        {'query': query}
    )
