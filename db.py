import mongoengine

host = 'mongodb+srv://admin:admin@thanhcluster-soioj.mongodb.net/project-I?retryWrites=true&w=majority'
db_name = "project-I"
user_name = "admin"
password = "admin"


def connect():
    mongoengine.connect(
        db_name, 
        host='mongodb+srv://admin:admin@thanhcluster-soioj.mongodb.net/project-I?retryWrites=true&w=majority',
        username='admin',
        password='admin'
    )
    