import uuid

from django.db import models

from Inventory.models import (
    VehicleModel,
    SpareParts,
)
from core.models import EmployeeProfile


class ServiceTypes(models.Model):
    service_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    service_name = models.CharField(max_length=255)
    service_etc = models.CharField(max_length=255)
    service_cost = models.FloatField()
    spare_parts = models.ManyToManyField(SpareParts)

    def __str__(self):
        return self.service_name


class VehicleService(models.Model):
    vehicle_no = models.CharField(max_length=50)
    model_id = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE
    )
    color = models.CharField(max_length=50)
    manufacture_year = models.DateField()
    service_types = models.ManyToManyField(ServiceTypes)

    def __str__(self):
        return self.vehicle_no


class Customer(models.Model):
    customer_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    vehicle_no = models.ForeignKey(
        VehicleService,
        on_delete=models.CASCADE
    )
    check_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


class Order(models.Model):
    STATUS_OPTIONS = (
        ('PND', 'Pending'),
        ('INP', 'In Progress'),
        ('COM', 'Complete'),
        ('BIL', 'Billed'),
    )
    
    order_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    engineer = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=150,
        choices=STATUS_OPTIONS,
    )
    additional_parts = models.ManyToManyField(
        SpareParts,
        blank=True,
        null=True
    )
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.customer_name


class Billing(models.Model):
    invoice_id = models.CharField(
        primary_key=True,
        max_length=255
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    vehicle_out = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    tax = models.FloatField()
    gross_total = models.FloatField()

    def __str__(self):
        return self.invoice_id
