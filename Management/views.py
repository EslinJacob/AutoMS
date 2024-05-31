from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required

from .models import (
    ServiceTypes,
    VehicleService,
    Order,
    Billing,
)
from .forms import (
    NewServiceTypeForm,
    EditServiceTypeForm,
    NewVehicleServiceForm,
    NewCustomerForm,
    PlaceOrderForm,
)
from core.models import EmployeeProfile
from core.utils import (
    check_employee_type,
    generate_invoice,
)


TYPE_LIST = ['management', 'mgmt']


@login_required
def management_home(request):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    orders = Order.objects.filter(
        status__in=['PND', 'INP', 'COM']
    )
    return render(
        request,
        'Management/management_home.html',
        {'orders': orders,}
    )


@login_required
def new_servicetypes_form(request):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    if request.method == 'POST':
        form = NewServiceTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('management:all_servicetypes')
    form = NewServiceTypeForm()

    return render(
        request,
        'Management/new_servicetypes.html',
        {'form': form,}
    ) 


@login_required
def all_servicetypes(request):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    servicetypes = ServiceTypes.objects.all()
    return render(
        request,
        'Management/all_servicetypes.html',
        {'servicetypes': servicetypes,}
    )


@login_required
def edit_servicetypes_form(request, pk):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    service = get_object_or_404(ServiceTypes, service_id=pk)
    if request.method == 'POST':
        form = EditServiceTypeForm(
            request.POST, 
            instance=service,
        )
        if form.is_valid():
            form.save()
            return redirect('management:all_servicetypes')
    form = EditServiceTypeForm(instance=service)
    return render(
        request,
        'Management/edit_servicetypes.html',
        {'form': form,}
    )


@login_required
def delete_servicetype(request, pk):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    service = get_object_or_404(ServiceTypes, service_id=pk)
    service.delete()
    return redirect('management:all_servicetypes')


@login_required
def new_vehicleservice_form(request):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    errors = None
    if request.method == 'POST':
        form = NewVehicleServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:new_customer')
        errors = form.errors
    form = NewVehicleServiceForm()
    return render(
        request,
        'Management/new_vehicleservice.html',
        {
            'form': form,
            'errors': errors,
        }
    )


@login_required
def new_customer_form(request):
    user = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    errors = None
    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:place_order')
        errors = form.errors
    form = NewCustomerForm()

    return render(
        request,
        'Management/new_customer.html',
        {
            'form': form,
            'errors': errors,
        }
    )


@login_required
def all_vehicleservice(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    vehicles = VehicleService.objects.all()
    return render(
        request,
        'Management/all_vehicleservice.html',
        {'vehicles': vehicles}
    )


@login_required
def place_order(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    errors = None
    if request.method == 'POST':
        form = PlaceOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management:management_home')
        errors = form.errors
    form = PlaceOrderForm()
    return render(
        request,
        'Management/place_order.html',
        {
            'form': form,
            'errors': errors,
        }
    )


@login_required
def checkout_order(request, pk):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    order = get_object_or_404(Order, pk=pk)
    if order.status != 'COM':
        return redirect('management:checkout_fail')
    total_costs = {
        'additional_parts': {},
        'service_types': {},
        'service_parts': {},
        'amount': {},
    }
    tax_rate = 0.18
    additional_parts = order.additional_parts.all()
    service_types = order.customer.vehicle_no.service_types.all()
    for part in additional_parts:
        total_costs['additional_parts'][part.part_name] = part.cost
    for types in service_types:
        total_costs['service_types'][types.service_name] = types.service_cost
        service_type_parts = types.spare_parts.all()
        for type_parts in service_type_parts:
            total_costs['service_parts'][type_parts.part_name] = type_parts.cost
    total_sum = sum(sum(costs.values()) for costs in total_costs.values())
    tax_amount = total_sum * tax_rate
    total_with_tax = total_sum + tax_amount
    total_costs['amount']['tax'] = tax_amount
    total_costs['amount']['total'] = total_with_tax
    invoice_number = generate_invoice(order)
    order_bill = Billing.objects.create(
        invoice_id=invoice_number,
        order=order,
        total=total_sum,
        tax=tax_amount,
        gross_total=total_with_tax
    )
    order_bill.save()
    order.status='BIL'
    order.save()
    
    return render(request, 'Management/checkout_order.html', {'data': total_costs,})


@login_required
def checkout_fail(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    return render(request, 'Management/checkout_fail.html')