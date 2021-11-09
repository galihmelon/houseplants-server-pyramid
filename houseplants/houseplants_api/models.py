from datetime import date, timedelta

from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class WateringLog(models.Model):
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE
    )
    water_date = models.DateField(auto_now_add=True)
    next_suggested_date = models.DateField()

    def __str__(self):
        return f'{self.plant.name} may need water on {self.next_suggested_date}'

    def save(self, *args, **kwargs):
        # self.next_suggested_date = date.today() + timedelta(7)
        super().save(*args, **kwargs)
