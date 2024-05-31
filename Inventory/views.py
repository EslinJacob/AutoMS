from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import (
    VehicleModel,
    SpareParts,
)
from .forms import (
    NewVehicleForm,
    EditVehicleForm,
    NewSparePartsForm,
    EditSparePartsForm,
)
from core.models import EmployeeProfile
from core.utils import check_employee_type


TYPE_LIST = ['inventory', 'inve']


@login_required
def inventory_home(request):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')

    dropdown = VehicleModel.objects.all()
    recent_parts = SpareParts.objects.order_by('-created_at')[:10]
    return render(
        request,
        'Inventory/inventory_home.html',
        {
            'dropdown': dropdown,
            'recent_parts': recent_parts,
        }
    )


@login_required
def filtered_parts(request, model):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    model = VehicleModel.objects.get(model_name=model)
    queryset = SpareParts.objects.filter(vehicle_model=model).order_by('-created_at')
    dropdown = VehicleModel.objects.all()
    return render(
        request,
        'Inventory/filtered_parts.html',
        {
            'dropdown': dropdown,
            'filtered_parts': queryset,
        }
    )


@login_required
def all_vehicles(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    vehicles = VehicleModel.objects.all()
    return render(
        request,
        'Inventory/all_vehicles.html',
        {'vehicles': vehicles}
    )


@login_required
def new_vehicle_form(request):
    if request.method == 'POST':
        form = NewVehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory:all_vehicles')
    form = NewVehicleForm()
    return render(
        request,
        'Inventory/new_vehicle.html',
        {'form': form,}
    )

def edit_vehicle_form(request, pk):
    vehicle = get_object_or_404(VehicleModel, id=pk)

    if request.method == 'POST':
        form = EditVehicleForm(
            request.POST, 
            instance=vehicle,
        )
        if form.is_valid():
            form.save()
            return redirect('inventory:all_vehicles')
        
    else:
        form = EditVehicleForm(instance=vehicle)

    return render(
        request,
        'Inventory/edit_vehicle.html',
        {'form': form,}
    )


@login_required
def delete_vehicle(request, pk):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')

    vehicle = get_object_or_404(VehicleModel, pk=pk)
    vehicle.delete()
    return redirect('inventory:all_vehicles')


@login_required
def all_spareparts(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    spares = SpareParts.objects.all()
    return render(
        request,
        'Inventory/all_spareparts.html',
        {'spares': spares}
    )


@login_required
def new_spareparts_form(request):
    if request.method == 'POST':
        form = NewSparePartsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inventory:all_spareparts')
    form = NewSparePartsForm()
    return render(
        request,
        'Inventory/new_spareparts.html',
        {'form': form,}
    )


@login_required
def edit_spareparts_form(request, pk):
    spareparts = get_object_or_404(SpareParts, pk=pk)
    print(f"CURRENT PART: {spareparts}")

    if request.method == 'POST':
        print(request.POST)
        form = EditSparePartsForm(
            request.POST, 
            instance=spareparts,
        )
        if form.is_valid():
            form.save()
            return redirect('inventory:all_spareparts')
    form = EditSparePartsForm(instance=spareparts)

    return render(
        request,
        'Inventory/edit_spareparts.html',
        {'form': form,}
    )


@login_required
def delete_part(request, pk):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')

    part = get_object_or_404(SpareParts, pk=pk)
    part.delete()
    return redirect('inventory:all_spareparts')