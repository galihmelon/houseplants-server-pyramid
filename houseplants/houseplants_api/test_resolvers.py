from datetime import date, timedelta
import pytest

from .resolvers import (
    resolve_all_plants,
    resolve_plants_to_care,
    resolve_water_plant,
)
from .test_factories import PlantFactory, WateringLogFactory


pytestmark = pytest.mark.django_db

def test_resolve_all_plants():
    plant_1 = PlantFactory()
    plant_2 = PlantFactory()
    result = resolve_all_plants()

    assert len(result) == 2
    plant_ids = result.values_list('id', flat=True)
    assert set(plant_ids) == set([plant_1.id, plant_2.id])


def test_resolve_plants_to_care_with_no_plants():
    result = resolve_plants_to_care()

    assert len(result) == 0


def test_resolve_plants_to_care_with_plants_and_no_logs():
    plant = PlantFactory()

    result = resolve_plants_to_care()

    assert len(result) == 1
    assert plant.id in result.values_list('id', flat=True)


def test_resolve_plants_to_care_with_watering_logs():
    log_a = WateringLogFactory(next_suggested_date=date.today())
    log_b = WateringLogFactory(next_suggested_date=date.today() - timedelta(days=3))
    log_c = WateringLogFactory(next_suggested_date=date.today() + timedelta(days=3))

    result = resolve_plants_to_care()

    assert len(result) == 2
    plant_ids = result.values_list('id', flat=True)
    assert set(plant_ids) == set([log_a.plant.id, log_b.plant.id])

    care_types = result.values_list('care_type', flat=True)
    assert set(care_types) == set(['water'])


def test_resolve_water_plant():
    PlantFactory(id=123)

    result = resolve_water_plant(plant_id=123)

    assert result.plant.id == 123
    assert result.water_date == date.today()
