from mongoengine import *
from mongoengine.queryset.visitor import Q
from models.user import User
from models.product import Product
from models.order import Order
import db
import json
import datetime

def unix_time_millis():
  dt = datetime.datetime.now()
  epoch = datetime.datetime.utcfromtimestamp(0)
  return int((dt - epoch).total_seconds() * 1000.0)

def create_user(email, password, firstname, lastname, phone, address):
    all_user = User.objects(email=email)

    if len(all_user) > 0:
        return False
    else:
        try:
            new_user = User(
                email = email,
                password = password,
                firstname = firstname,
                lastname = lastname,
                phone = phone,
                address= address
            ) 
            new_user.save()
            return True
        except:
            return False
        

def validate_user(email, password):
    found_user = User.objects(email=email,password=password)
    if found_user:
        found_user = User.objects.get(email=email,password=password)
        return found_user
    else:
        return False

def get_user(user_id):
    found_user = User.objects.with_id(user_id)
    if found_user:
        return found_user
    else:
        return False

def update_info(user_id, firstname, lastname, phone, address):
    update_user = User.objects.with_id(user_id)
    if update_user:
        update_user.update(set__firstname=firstname)
        update_user.update(set__lastname=lastname)
        update_user.update(set__phone=phone)
        update_user.update(set__address=address)
        return True
    else:
        return False

def update_password(user_id, password, new_password):
    update_user = User.objects(id=user_id, password=password)
    if update_user:
        update_user = User.objects.get(id=user_id, password=password)
        update_user.update(set__password=new_password)
        return True
    else:
        return False

def create_product(image, name, category, product_type, description, price, size):
    try:
        new_product = Product(
            image = image,
            name = name,
            category = category,
            product_type = product_type,
            description = description,
            price = price,
            size = size
        ) 
        new_product.save()
        return True
    except:
        return False

def get_product(category):
    found_products = Product.objects(category=category)
    products = []
    for p in found_products:
        products.append(p.to_dict())
    return products

def create_order(user_id, fullname, email, phone, address, guide_info, total_price, total_quantity, item_list):
    found_order = Order.objects(user_id=user_id, status="Chờ duyệt")
    if found_order:
        return False
    order_time = unix_time_millis()
    # prep_time = order_time + 5*60*1000
    # bake_time = prep_time + 20*60*1000
    status = "Chờ duyệt"
    new_order = Order(
        user_id=user_id,
        fullname=fullname,
        email=email,
        phone=phone,
        address=address,
        guide_info=guide_info,
        total_price=total_price,
        total_quantity=total_quantity,
        status=status,
        order_time=order_time,
        # prep_time=prep_time,
        # bake_time=bake_time,
        item_list=item_list
    )
    new_order.save()
    return True

# def dump(obj):
#     for attr in dir(obj):
#         if hasattr( obj, attr ):
#             print( "obj.%s = %s" % (attr, getattr(obj, attr)))

def get_user_order(user_id):
    found_order = Order.objects(user_id=user_id)
    orders = []
    for order in found_order: 
        new_item_list = []
        for item in order.to_dict()['item_list']:
            new_item_list.append(item.id)
        order['item_list'] = new_item_list
        orders.append(order.to_dict())
    return orders

def get_order(status):
    if status == "Đã hoàn thành":
        found_order = Order.objects(Q(status=status) | Q(status="Đã hủy"))
    else:
        found_order = Order.objects(status=status)
    orders = []
    for order in found_order: 
        new_item_list = []
        for item in order.to_dict()['item_list']:
            new_item_list.append(item.id)
        order['item_list'] = new_item_list
        orders.append(order.to_dict())
    return orders

def accept_order(order_id):
    found_order = Order.objects.with_id(order_id)
    if found_order:
        accept_time = unix_time_millis()
        prep_time = accept_time + 5*60*1000
        bake_time = prep_time + 20*60*1000
        found_order.update(set__status="Đang thực hiện")
        found_order.update(set__accept_time=accept_time)
        found_order.update(set__prep_time=prep_time)
        found_order.update(set__bake_time=bake_time)
        return True
    return False

def decline_order(order_id):
    found_order = Order.objects.with_id(order_id)
    if found_order:
        accept_time = unix_time_millis()
        prep_time = accept_time
        bake_time = accept_time
        found_order.update(set__status="Đã hủy")
        found_order.update(set__accept_time=accept_time)
        found_order.update(set__prep_time=prep_time)
        found_order.update(set__bake_time=bake_time)
        return True
    return False

def update_order(order_id, state):
    found_order = Order.objects.with_id(order_id)
    if found_order:
        if state == "updatePrep":
            prep_time = unix_time_millis()
            found_order.update(set__prep_time=prep_time)
        elif state == "updateBake":
            bake_time = unix_time_millis()
            found_order.update(set__bake_time=bake_time)
        elif state == "done":
            found_order.update(set__status="Đã hoàn thành")
        return True
    return False

def update_order_info(order_id, order_details):
    found_order = Order.objects.with_id(order_id)
    if found_order:
        found_order.update(__raw__={'$set': order_details})
        # print({*order_details})
        return True
    return False

def get_accepted_order(phone):
    found_order = Order.objects(phone=phone, status="Đang thực hiện")
    if found_order:
        orders = []
        for order in found_order: 
            new_item_list = []
            for item in order.to_dict()['item_list']:
                new_item_list.append(item.id)
            order['item_list'] = new_item_list
            orders.append(order.to_dict())
        return orders
    return False

if __name__ == "__main__":

    db.connect()

    # a = get_user("5ec704ddf885d72148cc5f32")
    # if a:   
    #     print(a)
    # else:
    #     print('not found')

    # product = {
    #     "image": "resize-bánh-cho-website-39.png",
    #     "name": "BÁNH SOCOLA",
    #     "category": "dessert",
    #     "product_type": "chocolate lava",
    #     "description": [],
    #     "price": 39000,
    #     "size": [],
    # }

    # new_product = Product(
    #     image = product["image"],
    #     name = product["name"],
    #     category = product["category"],
    #     product_type = product["product_type"],
    #     description = product["description"],
    #     price = product["price"],
    #     size = product["size"]
    # ) 
    # new_product = Product(**product)
    # new_product.save()
    
    # pizza = get_product("pizza")
    # print(json.dumps(pizza[0].to_json(),ensure_ascii=False))

    # print(unix_time_millis())

    # order = get_user_order("5ecd41a4f885d767a09fb4eb")
    # print(order[0]['item_list'])
    # found_order = Order.objects(status="Đang thực hiện")
    # for order in found_order:
    #     order.update(set__status="Đã hoàn thành")
