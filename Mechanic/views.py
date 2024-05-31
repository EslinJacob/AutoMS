from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import UpdateOrderForm
from core.utils import check_employee_type
from core.models import EmployeeProfile
from Management.models import Order


TYPE_LIST = ['mechanic', 'mech']

@login_required
def mechanic_home(request):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    orders = Order.objects.filter(
        Q(engineer=user_profile) & Q(status__in=['PND', 'INP'])
    )
    return render(
        request,
        'Mechanic/mechanic_home.html',
        {'orders': orders,}
    )


@login_required
def update_order(request, pk):
    user_profile = EmployeeProfile.objects.get(employee=request.user)
    flag = check_employee_type(user_profile, TYPE_LIST)
    if not flag:
        return redirect('core:unauthorised')
    errors = None
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('mechanic:mechanic_home')
        errors = form.errors
    form = UpdateOrderForm(instance=order)
    return render(
        request,
        'Mechanic/update_order.html',
        {
            'form': form,
            'errors': errors,
        }
    )
