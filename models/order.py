from mongoengine import *
from models.helper import mongo_to_dict

class CartItem(Document):
    product_id: StringField()
    category: StringField()
    name: StringField()
    size: StringField(default="")
    option: ListField(StringField())
    price: IntField()
    quantity: IntField()

    def to_dict(self):
        return mongo_to_dict(self)

class Order(Document):
    user_id = StringField()
    fullname = StringField()
    email = EmailField()
    phone = StringField()
    address = StringField()
    guide_info = StringField()
    total_price = IntField()
    total_quantity = IntField()
    status = StringField()
    order_time = IntField(default=0)
    accept_time = IntField(default=0)
    prep_time = IntField(default=0)
    bake_time = IntField(default=0)
    item_list = ListField(ReferenceField(CartItem))

    def to_dict(self):
        return mongo_to_dict(self)
    
