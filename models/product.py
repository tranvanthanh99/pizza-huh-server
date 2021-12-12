from mongoengine import *
from models.helper import mongo_to_dict

class Product(Document):
    image = StringField(default="")
    name = StringField(default="")
    category = StringField()
    product_type = StringField()
    description = ListField(StringField())
    price = IntField()
    size = ListField(StringField())

    def to_dict(self):
        return mongo_to_dict(self)