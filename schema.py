from datetime import date, timedelta
import graphene
from graphene_django import DjangoObjectType

from houseplants_api.models import Plant, WateringLog
from houseplants_api.resolvers import (
    resolve_all_plants,
    resolve_plants_to_care,
    resolve_water_plant,
)


class PlantType(DjangoObjectType):
    class Meta:
        model = Plant
        fields = ("id", "name", "image_url", "description")


class WateringLogType(DjangoObjectType):
    class Meta:
        model = WateringLog
        fields = ("plant", "water_date", "next_suggested_date")


class Query(graphene.ObjectType):
    all_plants = graphene.List(PlantType)
    plants_to_care = graphene.List(PlantType)

    def resolve_all_plants(root, info):
        return resolve_all_plants()

    def resolve_plants_to_care(root, info):
        return resolve_plants_to_care()


class WaterPlantMutation(graphene.Mutation):
    class Arguments:
        plant_id = graphene.ID()

    watering_log = graphene.Field(WateringLogType)

    @classmethod
    def mutate(cls, root, info, plant_id):
        log = resolve_water_plant(plant_id)
        return WaterPlantMutation(watering_log=log)


class Mutation(graphene.ObjectType):
    water_plant = WaterPlantMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
