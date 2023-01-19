import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType
from mongoengine import DoesNotExist

from models import (Element as ElementModel, Plane as PlaneModel, PlanePackage as PlanePackageModel)

class ElementType(MongoengineObjectType):
    class Meta:
        model = ElementModel
        interfaces = (Node,)

class PlaneType(MongoengineObjectType):
    class Meta:
        model = PlaneModel
        interfaces = (Node,)

class PlanePackageType(MongoengineObjectType):
    class Meta:
        model = PlanePackageModel
        interfaces = (Node,)

class Query(graphene.ObjectType):
    package = graphene.Field(PlanePackageType, name=graphene.String())

    def resolve_package(parent, info, name):
        return PlanePackageModel.objects.filter(name=name).first()

    all_packages = graphene.List(PlanePackageType)

    def resolve_all_packages(parent, info):
        return PlanePackageModel.objects

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

class PlanePackageInput(graphene.InputObjectType):
    name = graphene.String()
    planes = graphene.List(PlaneInput)
    topPlane= graphene.String()

class CreatePlanePackage(graphene.Mutation):
    planePackage = graphene.Field(PlanePackageType)

    class Arguments:
        planePackage_data = PlanePackageInput(required = True)

    def mutate(self, info, planePackage_data=None):
        planes = []
        for plane_data in planePackage_data.planes:
            elements = []
            for element_data in plane_data.elements:
                elements.append(ElementModel(
                    name = element_data.name,
                    description = element_data.description,
                    posX = element_data.posX,
                    posY = element_data.posY
                ))
            planes.append(PlaneModel(
                name=plane_data.name,
                height=plane_data.height,
                width=plane_data.width,
                elements=elements
            ))
        planePackage = PlanePackageModel(
            name=planePackage_data.name,
            topPlane=planePackage_data.topPlane,
            planes=planes
        )
        planePackage.save()

        return CreatePlanePackage(planePackage=planePackage)

class UpdatePlanePackage(graphene.Mutation):
    planePackage = graphene.Field(PlanePackageType)

    class Arguments:
        planePackage_data = PlanePackageInput(required = True)

    def mutate(self, info, planePackage_data=None):
        planePackage = PlanePackageModel.objects.get(name=planePackage_data.name)
        planes = []
        for plane_data in planePackage_data.planes:
            elements = []
            for element_data in plane_data.elements:
                elements.append(ElementModel(
                    name = element_data.name,
                    description = element_data.description,
                    posX = element_data.posX,
                    posY = element_data.posY
                ))
            planes.append(PlaneModel(
                name=plane_data.name,
                height=plane_data.height,
                width=plane_data.width,
                elements=elements
            ))
        planePackage.planes = planes
        planePackage.topPlane = planePackage_data.topPlane
        planePackage.save()

        return UpdatePlanePackage(planePackage=planePackage)

class DeletePlanePackage(graphene.Mutation):
    class Arguments:
        name = graphene.String(required = True)

    success = graphene.Boolean()

    def mutate(self, info, name):
        try:
            PlanePackageModel.objects.get(name=name).delete()
            success = True
        except DoesNotExist:
            success = False

        return DeletePlanePackage(success = success)

class Mutations(graphene.ObjectType):
    create_plane_package = CreatePlanePackage.Field()
    update_plane_package = UpdatePlanePackage.Field()
    delete_plane_package = DeletePlanePackage.Field()

schema = graphene.Schema(query=Query, mutation=Mutations, types=[PlanePackageType])