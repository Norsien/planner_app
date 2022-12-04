from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, ListField, EmbeddedDocumentField

class Element(EmbeddedDocument):
    name: StringField = StringField()
    description: StringField = StringField()
    posX: IntField = IntField()
    posY: IntField = IntField()

class Plane(Document):
    meta: dict[str, str] = {'collection': 'planes'}
    name: StringField = StringField(unique = True)
    height: IntField = IntField(min_value=0, max_value=100000, default=800, null=False)
    width: IntField = IntField(min_value=0, max_value=100000, default=1200, null=False)
    elements: ListField = ListField(EmbeddedDocumentField(Element))

# class PlanePackage(Document):
#     meta: dict[str, str] = {'collection': 'plane'}
#     name: StringField = StringField(unique = True)
#     planes: ListField = ListField(EmbeddedDocument(Plane))

