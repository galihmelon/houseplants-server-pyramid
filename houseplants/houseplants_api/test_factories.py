from datetime import date, timedelta
import factory

from .models import Plant, CleaningLog, WateringLog


class PlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plant

    name = factory.Faker('name')
    description = factory.Faker('text')
    image_url = factory.Faker('image_url')


class CleaningLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CleaningLog

    plant = factory.SubFactory(PlantFactory)
    next_suggested_date = date.today() + timedelta(days=7)


class WateringLogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WateringLog

    plant = factory.SubFactory(PlantFactory)
    next_suggested_date = date.today() + timedelta(days=7)
