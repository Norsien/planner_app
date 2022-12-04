import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from mongoengine import DoesNotExist

from models import (Plane as PlaneModel, Element as ElementModel)

class PlaneType(MongoengineObjectType):
    class Meta:
        model = PlaneModel
        interfaces = (Node,)

class ElementType(MongoengineObjectType):
    class Meta:
        model = ElementModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    plane = graphene.Field(PlaneType, name=graphene.String())
    all_planes = graphene.List(PlaneType)
    all_planes_2 = MongoengineConnectionField(PlaneType)

    def resolve_all_planes(parent, info):
        return PlaneModel.objects

    def resolve_plane(parent, info, name):
        return PlaneModel.objects.filter(name=name).first()


# Mutations
@staticmethod
def id_from_global(id):
    if len(id) > 24:
        return Node.from_global_id(id)[1]
    return id

class ElementInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    posX = graphene.Int()
    posY = graphene.Int()
    id = graphene.ID()

class PlaneInput(graphene.InputObjectType):
    name = graphene.String()
    height = graphene.Int()
    width = graphene.Int()
    elements = graphene.List(ElementInput)
    id = graphene.ID()

class CreatePlane(graphene.Mutation):
    plane = graphene.Field(PlaneType)

    class Arguments:
        plane_data = PlaneInput(required = True)

    def mutate(self, info, plane_data=None):
        elements = []
        for element_data in plane_data.elements:
            elements.append(ElementModel(
                name = element_data.name,
                description = element_data.description,
                posX = element_data.posX,
                posY = element_data.posY
            ))
        plane = PlaneModel(
            name=plane_data.name,
            height=plane_data.height,
            width=plane_data.width,
            elements=elements
        )
        plane.save()

        return CreatePlane(plane=plane)

class UpdatePlane(graphene.Mutation):
    plane = graphene.Field(PlaneType)

    class Arguments:
        plane_data = PlaneInput(required = True)

    def mutate(self, info, plane_data=None):
        plane = PlaneModel.objects.get(name=plane_data.name)
        if plane_data.elements:
            elements = []
            for element_data in plane_data.elements:
                elements.append(ElementModel(
                    name = element_data.name,
                    description = element_data.description,
                    posX = element_data.posX,
                    posY = element_data.posY
                ))
            plane.elements = elements
        if plane_data.name:
            plane.name = plane_data.name
        if plane_data.height:
            plane.height = plane_data.height
        if plane_data.width:
            plane.width = plane_data.width
        plane.save()

        return UpdatePlane(plane=plane)

class DeletePlane(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)

    success = graphene.Boolean()

    def mutate(self, info, name):
        try:
            PlaneModel.objects.get(name=name).delete()
            success = True
        except DoesNotExist:
            success = False

        return DeletePlane(success = success)

class Mutations(graphene.ObjectType):
    create_plane = CreatePlane.Field()
    update_plane = UpdatePlane.Field()
    delete_plane = DeletePlane.Field()

schema = graphene.Schema(query=Query, mutation=Mutations, types=[PlaneType])