from datetime import date, timedelta
from django.db.models import Max, CharField, Value

from .models import Plant, CleaningLog, WateringLog

from .actions import (
    clean_plant,
    get_all_plants,
    get_plants_to_care,
    water_plant,
)

def resolve_all_plants():
    return get_all_plants()


def resolve_plants_to_care():
    return get_plants_to_care()


def resolve_clean_plant(plant_id):
    return clean_plant(plant_id)


def resolve_water_plant(plant_id):
    return water_plant(plant_id)
