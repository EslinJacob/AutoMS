from django.db import models
from django.contrib.auth.models import User


class EmployeeProfile(models.Model):
    EMPLOYEE_TYPE = (
        ('mgmt', 'management'),
        ('mech', 'mechanic'),
        ('inve', 'inventory'),
        ('supe', 'supervisor'),
    )
    employee = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    employee_type = models.CharField(
        max_length=255,
        choices=EMPLOYEE_TYPE,
    )

    def __str__(self):
        return self.employee.username
