from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, ListField, EmbeddedDocumentField

class Element(EmbeddedDocument):
    name: StringField = StringField(required=True)
    description: StringField = StringField(required=True)
    posX: IntField = IntField(required=True)
    posY: IntField = IntField(required=True)

class Plane(EmbeddedDocument):
    name: StringField = StringField()
    height: IntField = IntField(min_value=0, max_value=100000, default=800, null=False, required=True)
    width: IntField = IntField(min_value=0, max_value=100000, default=1200, null=False, required=True)
    elements: ListField = ListField(EmbeddedDocumentField(Element))

class PlanePackage(Document):
    meta: dict[str, str] = {'collection': 'planePackages'}
    name: StringField = StringField(unique = True, required=True)
    planes: ListField = ListField(EmbeddedDocumentField(Plane), required=True)
    topPlane: StringField = StringField(required=True)

