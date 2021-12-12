from flask import Flask, render_template, jsonify, request, Response
from mongoengine import *
from models.user import User
from models.product import Product
from flask_cors import CORS
import db
import service

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

db.connect()

@app.route('/get-user/<user_id>', methods = ['GET'])
def get_user(user_id):
  res = service.get_user(user_id)
  if res:
    return jsonify(
      user_id=str(res.id),
      email=res.email, 
      role=res.role,
      firstname=res.firstname, 
      lastname=res.lastname, 
      phone=res.phone, 
      address=res.address
    ) , 200
  else:
    return jsonify({
      "success": False,
      "error": "Invalid user id"
    }) , 200
    

@app.route('/register', methods = ['POST'])
def register():
  
  email = request.json['email']
  password = request.json['password']
  firstname = request.json['firstname']
  lastname = request.json['lastname']
  phone = request.json['phone']
  address = request.json['address']

  res = service.create_user(email, password, firstname, lastname, phone, address)
  if res:
    return jsonify({
      'success': 'true'
    }) , 200
  else: 
    return jsonify({
      'error' : 'invalid email'
    }), 201

@app.route('/login', methods = ['POST'])
def login():
  
  email = request.json['email']
  password = request.json['password']
  
  res = service.validate_user(email, password)
  
  if res:
    return jsonify(
      user_id=str(res.id),
      email=res.email, 
      role=res.role,
      firstname=res.firstname, 
      lastname=res.lastname, 
      phone=res.phone, 
      address=res.address
      ) , 200
  else: 
    found_user = User.objects(email=email)
    if found_user:
        return jsonify({'email': True, 'password': False}), 201
    return jsonify({'email': False, 'password': False}), 201

@app.route('/update-info', methods = ['POST'])
def update_info():
  
  user_id = request.json['user_id']
  firstname = request.json['firstname']
  lastname = request.json['lastname']
  phone = request.json['phone']
  address = request.json['address']
  
  res = service.update_info(user_id, firstname, lastname, phone, address)
  
  if res:
    return jsonify({'success': True}) , 200
  else: 
    return jsonify({'success': False}), 201

@app.route('/update-password', methods = ['POST'])
def update_password():
  
  user_id = request.json['user_id']
  password = request.json['password']
  new_password = request.json['newPassword']
  
  res = service.update_password(user_id, password, new_password)
  
  if res:
    return jsonify({'success': True}) , 200
  else: 
    return jsonify({'success': False}), 201

@app.route('/get-product/<category>')
def get_product(category):
  found_products = service.get_product(category)
  return jsonify({
    "product": found_products
  }), 200

@app.route('/create-order', methods=['POST'])
def create_order():
    user_id = request.json['user_id']
    fullname = request.json['fullname']
    email = request.json['email']
    phone = request.json['phone']
    address = request.json['address']
    guide_info = request.json['guide_info']
    total_price = request.json['total_price']
    total_quantity = request.json['total_quantity']
    item_list = request.json['item_list']
    res = service.create_order(user_id, fullname, email, phone, address, guide_info, total_price, total_quantity, item_list)
    if res:
      return jsonify({'success': True}) , 200
    else:
      return jsonify({'success': False}), 201

@app.route('/get-user-order/<user_id>')
def get_user_order(user_id):
    found_order = service.get_user_order(user_id)
    return jsonify({'order_list': found_order}) , 200

@app.route('/get-order/<status>')
def get_done_order(status):
    found_order = service.get_order(status)
    return jsonify({'order_list': found_order}) , 200

@app.route('/accept-order/<order_id>')
def accept_order(order_id):
    res = service.accept_order(order_id)
    if res:
      return jsonify({'success': True}) , 200
    else:
      return jsonify({'success': False}), 201

@app.route('/update-order', methods=['POST'])
def update_order():
    order_id = request.json['order_id']
    state = request.json['state']
    res = service.update_order(order_id, state)
    if res:
      return jsonify({'success': True}) , 200
    else:
      return jsonify({'success': False}), 201

@app.route('/track-order/<phone>')
def track_order(phone):
    found_order = service.get_accepted_order(phone)
    if found_order:
      return jsonify({"order_list": found_order}), 200
    return jsonify({'success': False}), 201

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=False)
    