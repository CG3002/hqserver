'''
This file contains the Database ORMs of the hqserver
'''
from hqserver import app
from flask.ext.sqlalchemy import SQLAlchemy, before_models_committed
import time
import os
import views
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hari/test1.db'
# app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)

class Product(db.Model):
	__tablename__='Products'
	barcode=db.Column(db.Integer, primary_key=True)
	product_name=db.Column(db.String(32))
	description=db.Column(db.String(120))
	category=db.Column(db.String(32))
	manufacturer_name=db.Column(db.String(32))
	product_MRP=db.Column(db.Float)
	product_bundle_unit=db.Column(db.Integer)

	def __init__(self, **kwargs):
		self.barcode = kwargs.get('barcode')
		self.product_name = kwargs.get('product_name', None)
		self.description = kwargs.get('description', None)
		self.category = kwargs.get('category', None)
		self.manufacturer_name = kwargs.get('manufacturer_name', None)
		self.product_MRP = kwargs.get('product_MRP', 0)
		self.product_bundle_unit = kwargs.get('product_bundle_unit', 0)

	def __repr__(self):
		return '<Product Barcode: %r>' % self.barcode

	def serialize(self):
		return {
		'barcode' : self.barcode,
		'product_MRP' : self.product_MRP,
		'product_bundle_unit' : self.product_bundle_unit
		}



class Outlet(db.Model):
	__tablename__='Outlets'
	outlet_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
	outlet_name=db.Column(db.String(120))
	manager_name=db.Column(db.String(120))
	location=db.Column(db.String(120))
	outlet_server_ip=db.Column(db.String(120), unique=True)

	def __init__(self, **kwargs):
		self.outlet_id = kwargs.get('outlet_id')
		self.outlet_name = kwargs.get('outlet_name', None)
		self.manager_name = kwargs.get('manager_name', None)
		self.location = kwargs.get('location', None)
		self.outlet_server_ip = kwargs.get('outlet_server_ip', "http://127.0.0.1:8000/")

	def __repr__(self):
		return '<Outlet ID: %r>' % self.outlet_id


class RetailLink(db.Model):
	__tablename__='RetailLinks'
	barcode=db.Column(db.Integer, db.ForeignKey('Products.barcode', ondelete='SET NULL'), primary_key=True)
	outlet_id=db.Column(db.Integer, db.ForeignKey('Outlets.outlet_id', ondelete='SET NULL'), primary_key=True)
	product_max_stock=db.Column(db.Integer)
	product_min_stock=db.Column(db.Integer)
	outlet=db.relationship('Outlet',
        backref=db.backref('productsInOutlet', lazy='dynamic'))
	product=db.relationship('Product',
		backref=db.backref('outletsStockedby', lazy='dynamic'))

	def __init__(self, **kwargs):
		self.barcode=kwargs.get('barcode')
		self.outlet_id=kwargs.get('outlet_id')
		self.product_max_stock=kwargs.get('max_stock', 500)
		self.product_min_stock=kwargs.get('min_stock', 50)

	def __repr__(self):
		return '<RetailLink Barcode: %r, Outlet_ID: %r>' % (self.barcode, self.outlet_id)

class TransactionSync(db.Model):
	__tablename__= 'Retail Transaction Summary'
	barcode=db.Column(db.Integer, db.ForeignKey('Products.barcode', ondelete='SET NULL'), primary_key=True)
	outlet_id=db.Column(db.Integer, db.ForeignKey('Outlets.outlet_id', ondelete='SET NULL'), primary_key=True)
	timestamp=db.Column(db.Integer, primary_key=True)
	quantity_sold=db.Column(db.Integer)
	total_revenue=db.Column(db.Float)
	product=db.relationship('Product',
		backref=db.backref('transactionsAssociated', lazy='dynamic'))
	outlet=db.relationship('Outlet',
        backref=db.backref('transactionsOutlets', lazy='dynamic'))

	def __init__(self, **kwargs):
		self.barcode=kwargs.get('barcode')
		self.outlet_id=kwargs.get('outlet_id')
		self.timestamp=kwargs.get('timestamp')
		self.quantity_sold=kwargs.get('quantity_sold', 0)
		self.total_revenue=kwargs.get('total_revenue', 0)

class User(db.Model):
	__tablename__='Trolley Users'
	__table_args__= {'sqlite_autoincrement': True}
	user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
	email=db.Column(db.String(120), unique=True)
	pw_hash=db.Column(db.String(160), unique=True)
	name=db.Column(db.String(120))
	is_admin=db.Column(db.Boolean)

	def __init__(self, **kwargs):
		self.email=kwargs.get('email')
		if kwargs.get('password') is not None:
			self.set_password(kwargs.get('password'))
		self.name=kwargs.get('name', "")
		self.is_admin=kwargs.get('is_admin', False)

	def set_password(self, password):
		print "Here"
		print password
		print generate_password_hash(password)
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def __repr__(self):
		return '<Email: %r>' % (self.email)		

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_administrator(self):
		return self.is_admin

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.user_id)

class Trolley(db.Model):
	__tablename__='Trolley Details'
	__table_args__={'sqlite_autoincrement' : True}
	trolley_id=db.Column(db.Integer, db.ForeignKey('User Trolley Link.trolley_id', ondelete='SET NULL'), primary_key=True)
	barcode=db.Column(db.Integer, db.ForeignKey('Products.barcode', ondelete='SET NULL'), primary_key=True)
	quantity=db.Column(db.Integer)
	product=db.relationship('Product', backref='trolleys')

	def __init__(self, **kwargs):
		self.barcode=kwargs.get('barcode')
		self.quantity=kwargs.get('quantity')
		self.trolley_id=kwargs.get('trolley_id')
		

	@classmethod
	def create_trolley(cls, **kwargs):
		print "Here"
		trolley=kwargs.get('trolley')
		trolley_id=kwargs.get('trolley_id')
		for item in trolley:
			print item['barcode'], item['quantity']
			if item['barcode'] == "" or item['barcode'] is None:
				return False
			new_trolley=cls(barcode=item['barcode'], quantity=item['quantity'], trolley_id=trolley_id)
			db.session.add(new_trolley)
			db.session.commit()

class TrolleyLink(db.Model):
	__tablename__='User Trolley Link'
	trolley_id=db.Column(db.Integer, primary_key=True)
	user_id=db.Column(db.Integer, db.ForeignKey('Trolley Users.user_id', ondelete='SET NULL'))
	date_created=db.Column(db.DateTime)

	def __init__(self, **kwargs):
		self.user_id=kwargs.get('user_id')
		self.trolley_id=kwargs.get('trolley_id', None)
		self.date_created=datetime.datetime.now()
		if self.trolley_id is None:
			done=0
			while(done==0):
				trolley_id=randint(100000, 999999)
				existing_trolley=TrolleyLink.query.get(trolley_id)
				print existing_trolley
				if existing_trolley is None:
					self.trolley_id=trolley_id
					done=1
				else:
					done=0


def outlet_db_sync(sender, changes):
	for model, change in changes:
		if isinstance(model, RetailLink):
			if model.product is not None and model.outlet is not None:
				views.outlet_sync(model.product.barcode, change, model.outlet.outlet_id)
			elif model.barcode is not None and model.outlet_id is not None:
				views.outlet_sync(model.barcode, change, model.outlet_id)
		elif isinstance(model, Product):
			outlets_with_product=RetailLink.query.filter_by(barcode=model.barcode).all()
			for outlet in outlets_with_product:
				if change != "delete":
					views.outlet_sync(model.barcode, change, outlet.outlet_id)
				else:
					db.session.delete(outlet)

before_models_committed.connect(outlet_db_sync, sender=app)


