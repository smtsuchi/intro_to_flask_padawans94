from flask import Blueprint, request
from ..apiauthhelper import token_required
from app.models import User, Product, cart


shop = Blueprint('shop', __name__)

@shop.route('/api/products')
def getAllProducts():
    products = Product.query.all()

    return {
        'status': 'ok',
        'products': [p.to_dict() for p in products] 
    }

@shop.route('/api/products/<int:product_id>')
def getOneProduct(product_id):
    product = Product.query.get(product_id)
    return {
        'status': 'ok',
        'product': product.to_dict()
    }

@shop.route('/api/cart')
@token_required
def getCart(user):

    return {
        'status': 'ok',
        'cart': [p.to_dict() for p in user.getCart()]
        }

@shop.route('/api/cart/add', methods=["POST"])
@token_required
def addToCart(user):
    data = request.json
    product_id = data['productId']
    product = Product.query.get(product_id)
    user.addToCart(product)
    return {'status': 'ok','message': 'Succesfully added to cart.'}

@shop.route('/api/cart/remove', methods=["POST"])
@token_required
def removeFromCart(user):
    data = request.json
    product_id = data['productId']
    product = Product.query.get(product_id)
    user.removeFromCart(product)
    return {'status':'ok', 'message':'Successfully removed from cart.'}