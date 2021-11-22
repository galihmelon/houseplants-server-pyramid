from datetime import date, timedelta
from django.db.models import Max, CharField, Value

from .models import Plant, CleaningLog, WateringLog


def resolve_all_plants():
    return Plant.objects.all()


def resolve_plants_to_care():
    plants_to_clean = CleaningLog.objects.filter(next_suggested_date__lte=date.today()).values('plant').annotate(last_suggested_date=Max('next_suggested_date'))
    plants_without_cleaning_logs = Plant.objects.filter(cleaninglog__isnull=True)
    plants_to_clean = (
        Plant.objects
        .filter(id__in=(
            [plant['plant'] for plant in plants_to_clean]
            + [plant.id for plant in plants_without_cleaning_logs]
        ))
        .annotate(care_type=Value('clean', output_field=CharField()))
    )

    plants_to_water = WateringLog.objects.filter(next_suggested_date__lte=date.today()).values('plant').annotate(last_suggested_date=Max('next_suggested_date'))
    plants_without_watering_logs = Plant.objects.filter(wateringlog__isnull=True)
    plants_to_water = (
        Plant.objects
        .filter(id__in=(
            [plant['plant'] for plant in plants_to_water]
            + [plant.id for plant in plants_without_watering_logs]
        ))
        .annotate(care_type=Value('water', output_field=CharField()))
    )

    return plants_to_clean.union(plants_to_water)


def resolve_clean_plant(plant_id):
    plant = Plant.objects.get(id=plant_id)
    log = CleaningLog.objects.create(plant=plant, next_suggested_date=date.today() + timedelta(days=7))
    return log


def resolve_water_plant(plant_id):
    plant = Plant.objects.get(id=plant_id)
    log = WateringLog.objects.create(plant=plant, next_suggested_date=date.today() + timedelta(days=7))
    return log
