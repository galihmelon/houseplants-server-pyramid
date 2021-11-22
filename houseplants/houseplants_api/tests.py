from datetime import date, timedelta
import pytest
from graphene.test import Client

from schema import schema
from .test_factories import PlantFactory, CleaningLogFactory, WateringLogFactory


pytestmark = pytest.mark.django_db


def test_plants_to_care_query_with_no_plants():
    client = Client(schema)
    executed = client.execute(
        '''
        query {
            plantsToCare {
                id
                name
                imageUrl
                description
            }
        }
        '''
    )
    assert executed == {
        'data': {
            'plantsToCare': []
        }
    }


def test_plants_to_care_query_with_plants_and_no_logs():
    PlantFactory()

    client = Client(schema)
    executed = client.execute(
        '''
        query {
            plantsToCare {
                id
                name
                imageUrl
                description
            }
        }
        '''
    )
    plants_to_care = executed['data']['plantsToCare']
    # 1 result for watering and 1 result for cleaning
    assert len(plants_to_care) == 2


def test_plants_to_care_query_with_results():
    log_a = WateringLogFactory(next_suggested_date=date.today())
    log_b = WateringLogFactory(next_suggested_date=date.today() - timedelta(days=3))
    log_c = WateringLogFactory(next_suggested_date=date.today() + timedelta(days=3))

    CleaningLogFactory(plant=log_a.plant, next_suggested_date=date.today())
    CleaningLogFactory(plant=log_b.plant, next_suggested_date=date.today() - timedelta(days=3))
    CleaningLogFactory(plant=log_c.plant, next_suggested_date=date.today() + timedelta(days=3))

    client = Client(schema)
    executed = client.execute(
        '''
        query {
            plantsToCare {
                id
                name
                imageUrl
                description
            }
        }
        '''
    )
    plants_to_care = executed['data']['plantsToCare']
    assert len(plants_to_care) == 4

    plant_ids = [int(plant['id']) for plant in plants_to_care]
    assert set(plant_ids) == set([log_a.plant.id, log_b.plant.id])


def test_water_plant_mutation():
    PlantFactory(id=123)

    client = Client(schema)
    executed = client.execute(
        '''
        mutation {
            waterPlant(plantId: 123) {
                wateringLog {
                    plant {
                        id
                    }
                    nextSuggestedDate
                    waterDate
                }
            }
        }
        '''
    )
    log = executed['data']['waterPlant']['wateringLog']
    assert log['plant']['id'] == '123'
    assert log['waterDate'] == date.today().strftime('%Y-%m-%d')


def test_clean_plant_mutation():
    PlantFactory(id=123)

    client = Client(schema)
    executed = client.execute(
        '''
        mutation {
            cleanPlant(plantId: 123) {
                cleaningLog {
                    plant {
                        id
                    }
                    nextSuggestedDate
                    cleanDate
                }
            }
        }
        '''
    )
    log = executed['data']['cleanPlant']['cleaningLog']
    assert log['plant']['id'] == '123'
    assert log['cleanDate'] == date.today().strftime('%Y-%m-%d')
