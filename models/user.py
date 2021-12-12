from mongoengine import *

class User(Document):
    email = EmailField()
    password = StringField()
    role = StringField(default="user")
    firstname = StringField()
    lastname = StringField()
    phone = StringField()
    address = StringField()
    