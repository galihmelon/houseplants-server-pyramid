from datetime import date, timedelta
import pytest

from .test_factories import PlantFactory, CleaningLogFactory, WateringLogFactory
from .actions import (
    get_all_plants,
    get_plants_to_care,
    water_plant,
    clean_plant,
)

pytestmark = pytest.mark.django_db


def test_get_all_plants():
    plant_1 = PlantFactory()
    plant_2 = PlantFactory()
    result = get_all_plants()

    assert len(result) == 2
    plant_ids = result.values_list('id', flat=True)
    assert set(plant_ids) == set([plant_1.id, plant_2.id])


def test_get_plants_to_care_with_no_plants():
    result = get_plants_to_care()

    assert len(result) == 0


def test_resolve_plants_to_care_with_plants_and_no_logs():
    plant = PlantFactory()

    result = get_plants_to_care()

    assert len(result) == 2
    assert plant.id in result.values_list('id', flat=True)


def test_resolve_plants_to_care_with_watering_logs():
    log_a = WateringLogFactory(next_suggested_date=date.today())
    log_b = WateringLogFactory(next_suggested_date=date.today() - timedelta(days=3))
    log_c = WateringLogFactory(next_suggested_date=date.today() + timedelta(days=3))

    CleaningLogFactory(plant=log_a.plant, next_suggested_date=date.today())
    CleaningLogFactory(plant=log_b.plant, next_suggested_date=date.today() - timedelta(days=3))
    CleaningLogFactory(plant=log_c.plant, next_suggested_date=date.today() + timedelta(days=3))

    result = get_plants_to_care()

    num_plants_to_water = 2
    num_plants_to_clean = 2
    assert len(result) == num_plants_to_water + num_plants_to_clean
    plant_ids = result.values_list('id', flat=True)
    assert set(plant_ids) == set([log_a.plant.id, log_b.plant.id])

    care_types = [plant.care_type for plant in result]
    assert set(care_types) == set(['clean', 'water'])


def test_resolve_clean_plant():
    PlantFactory(id=123)

    result = clean_plant(plant_id=123)

    assert result.plant.id == 123
    assert result.clean_date == date.today()


def test_water_plant():
    PlantFactory(id=123)

    result = water_plant(plant_id=123)

    assert result.plant.id == 123
    assert result.water_date == date.today()