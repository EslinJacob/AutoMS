from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import EmployeeProfile
from .forms import (
    SignUpForm,
    EditUserForm,
    EditProfileForm,
)


def index(request):
    if request.user.is_authenticated:
        current_user = get_object_or_404(User, id=request.user.id)
        user_profile = EmployeeProfile.objects.get(employee=current_user)
        match user_profile.employee_type:
            case 'supervisor' | 'supe':
                return redirect('core:user_mgmt')
            case 'management' | 'mgmt':
                return redirect('management:management_home')
            case 'mechanic' | 'mech':
                return redirect('mechanic:mechanic_home')
            case 'inventory' | 'inve':
                return redirect('inventory:inventory_home')
            case _:
                return redirect('core:unauthorised')
    else:
        return render(
            request,
            "index.html",
        )


def unauthorised(request):
    return render(request, 'unauthorised.html')


@login_required
def user_mgmt(request):
    if not request.user.is_superuser:
        return redirect('core:unauthorised')
    employees = EmployeeProfile.objects.all()
    return render(
        request,
        'user_mgmt.html',
        {'employees': employees}
    )


@login_required
def signup(request):
    if not request.user.is_superuser:
        return redirect('core:unauthorised')
    errors = None

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            if (request.POST['employee_type'] == 'supervisor'
            or request.POST['employee_type'] == 'supe'):
                if request.user.is_superuser:
                    current_user.is_superuser = True
            current_user.save()
            EmployeeProfile.objects.create(
                employee=current_user,
                employee_type=request.POST['employee_type']
            )
            return redirect('core:user_mgmt')
        else:
            errors = form.errors

    form = SignUpForm()
    return render(
        request,
        'signup.html',
        {
            'form': form,
            'errors': errors
        }
    )


@login_required
def edit_employee(request, pk):
    if not request.user.is_superuser:
        return redirect('core:unauthorised')
    profile = get_object_or_404(EmployeeProfile, pk=pk)
    user = get_object_or_404(User, pk=profile.employee.id)
    user_errors = None
    profile_errors = None
    if request.method == 'POST':
        edit_user_form = EditUserForm(request.POST, instance=user)
        edit_profile_form = EditProfileForm(request.POST, instance=profile)

        if (edit_user_form.is_valid()
            and edit_profile_form.is_valid()):
            edit_user = edit_user_form.save(commit=False)
            if request.user.is_superuser:
                if (request.POST['employee_type'] == 'supervisor'
                or request.POST['employee_type'] == 'supe'):
                    edit_user.is_superuser = True
                else:
                    edit_user.is_superuser = False
            edit_user.save()
            edit_profile_form.save()
            return redirect('core:user_mgmt')
        user_errors = edit_user_form.errors
        profile_errors = edit_profile_form.errors
    userform = EditUserForm(instance=user)
    profileform = EditProfileForm(instance=profile)

    context = {
        'userform': userform,
        'profileform': profileform,
        'user_errors': user_errors,
        'profile_errors': profile_errors,
    }
    return render(
        request,
        'edit_user.html',
        context
    )


@login_required
def delete_employee(request, pk):
    if not request.user.is_superuser:
        return redirect('core:unauthorised')
    obj_instance = get_object_or_404(EmployeeProfile, pk=pk)
    username = obj_instance.employee.username
    user = User.objects.get(username=username)
    obj_instance.delete()
    user.delete()
    return redirect('core:user_mgmt')
