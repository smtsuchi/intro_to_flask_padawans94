from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


# class Followers(db.Model):
#     follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
#     followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)

user_pokemon = db.Table('user_pokemon',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id')),
)

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

# create our Models based off of our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)

    post = db.relationship("Post", backref='author', lazy=True)
    followed = db.relationship("User",
        primaryjoin = (followers.c.follower_id==id),
        secondaryjoin = (followers.c.followed_id==id),
        secondary = followers,
        backref = db.backref('followers', lazy='dynamic'),
        lazy = 'dynamic'
    )
    team = db.relationship("Pokemon",
        secondary = user_pokemon,
        backref='trainers',
        lazy = 'dynamic'
    )
    cart = db.relationship("Product",
        secondary = cart,
        backref = 'cart_users',
        lazy = 'dynamic'
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def follow(self, user):
        self.followed.append(user)
        db.session.commit()

    def unfollow(self, user):
        self.followed.remove(user)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }

    def getCart(self):
        list_of_tuples = db.session.query(cart).filter(cart.c.user_id ==self.id).all()
        return [Product.query.get(t[1]) for t in list_of_tuples]
    
    def saveToDB(self):
        db.session.commit()

    # get all the posts that I am following PLUS my own
    def get_followed_posts(self):
        # all the posts i am following
        followed = Post.query.join(followers, (Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.id)
        # get all my posts
        mine = Post.query.filter_by(user_id = self.id)
        # put them all together
        all = followed.union(mine).order_by(Post.date_created.desc())
        return all

    def addToCart(self, product):
        self.cart.append(product)
        db.session.commit()

    def removeFromCart(self, product):
        self.cart.remove(product)
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True)
    ability = db.Column(db.String)
    hp = db.Column(db.String)
    attack = db.Column(db.String)
    defense = db.Column(db.String)
    img_url = db.Column(db.String)
    def __init__(self, name, ability, hp, attack, defense, img_url):
        self.name = name
        self.ability = ability
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.img_url=img_url
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String(300))
    caption = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id

    def updatePostInfo(self, title, img_url, caption):
        self.title = title
        self.img_url = img_url
        self.caption = caption

    def save(self):
        db.session.add(self)
        db.session.commit()

    def saveUpdates(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'img_url': self.img_url,
            'date_created': self.date_created,
            'user_id': self.user_id,
            'author': self.author.username
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Numeric(10,2))

    def __init__(self, name,img, desc, price):
        self.product_name = name
        self.img_url = img
        self.description = desc
        self.price = price


    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'img_url': self.img_url,
            'description': self.description,
            'price': self.price
        }