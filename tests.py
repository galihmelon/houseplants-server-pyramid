from datetime import date, timedelta
import pytest
from graphene.test import Client

from schema import schema
from .test_factories import PlantFactory, WateringLogFactory


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
    assert len(plants_to_care) == 1


def test_plants_to_care_query_with_results():
    plan_a = WateringLogFactory(next_suggested_date=date.today())
    plan_b = WateringLogFactory(next_suggested_date=date.today() - timedelta(days=3))
    plan_c = WateringLogFactory(next_suggested_date=date.today() + timedelta(days=3))

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
    assert len(plants_to_care) == 2

    plant_ids = [int(plant['id']) for plant in plants_to_care]
    assert plant_ids == [plan_a.plant.id, plan_b.plant.id]


def test_water_plant_mutation():
    PlantFactory(id=1)

    client = Client(schema)
    executed = client.execute(
        '''
        mutation {
            waterPlant(plantId: 1) {
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
    assert log['plant']['id'] == '1'
    assert log['waterDate'] == date.today().strftime('%Y-%m-%d')
