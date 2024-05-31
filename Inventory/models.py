import uuid
import os
import shutil

from django.db import models
from django.utils import timezone
from django.conf import settings


class VehicleModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    model_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='static/media/vehicle_models'
    )
    log = models.FileField(
        upload_to='static/media/logs'
    )

    def save(self, *args, **kwargs):
        super(VehicleModel, self).save(*args, **kwargs)

        target_dir_img = f"{settings.BASE_DIR}/static/media/vehicle_models"
        image = self.image.path
        print(f"/n/nIMAGE: {image}/n/n")

        target_dir_log = f"{settings.BASE_DIR}/static/media/logs"
        log = self.log.path

        if not os.path.isfile(
            os.path.join(target_dir_img, os.path.basename(image))
        ):
            shutil.copy(image, target_dir_img)
            os.remove(image)

        if not os.path.isfile(
            os.path.join(target_dir_log, os.path.basename(log))
        ):
            shutil.copy(log, target_dir_log)
            os.remove(log)

    def __str__(self):
        return self.model_name


class SpareParts(models.Model):
    part_no = models.CharField(
        max_length=255,
        primary_key=True
    )
    part_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    cost = models.FloatField()
    vehicle_model = models.ForeignKey(
        VehicleModel,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.part_name
