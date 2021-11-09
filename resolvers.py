from datetime import date, timedelta
from django.db.models import Max

from .models import Plant, WateringLog


def resolve_all_plants():
    return Plant.objects.all()


def resolve_plants_to_care():
    plants = WateringLog.objects.filter(next_suggested_date__lte=date.today()).values('plant').annotate(last_suggested_date=Max('next_suggested_date'))
    plants_without_logs = Plant.objects.filter(wateringlog__isnull=True)
    return Plant.objects.filter(id__in=([plant['plant'] for plant in plants] + [plant.id for plant in plants_without_logs]))


def resolve_water_plant(plant_id):
    plant = Plant.objects.get(id=plant_id)
    log = WateringLog.objects.create(plant=plant, next_suggested_date=date.today() + timedelta(days=7))
    return log
