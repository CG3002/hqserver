'''
This file contains the Database ORMs of the hqserver
'''
from hqserver import app
from flask.ext.sqlalchemy import SQLAlchemy, before_models_committed
import time
import os
import views

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hari/test.db'
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
	barcode=db.Column(db.Integer, db.ForeignKey('Products.barcode'), primary_key=True)
	outlet_id=db.Column(db.Integer, db.ForeignKey('Outlets.outlet_id'), primary_key=True)
	product_max_stock=db.Column(db.Integer)
	product_min_stock=db.Column(db.Integer)
	outlet=db.relationship('Outlet',
        backref=db.backref('productsInOutlet', lazy='dynamic'))
	product=db.relationship('Product',
		backref=db.backref('outletsStockedby', lazy='dynamic'))

	def __init__(self, **kwargs):
		self.barcode=kwargs.get('barcode')
		self.outlet_id=kwargs.get('outlet_id', 1)
		self.product_max_stock=kwargs.get('max_stock', 0)
		self.product_min_stock=kwargs.get('min_stock', 0)

	def __repr__(self):
		return '<RetailLink Barcode: %r, Outlet_ID: %r>' % (self.barcode, self.outlet_id)


def outlet_db_sync(sender, changes):
	for model, change in changes:
		if isinstance(model, RetailLink):
			if change == "insert" or change == "delete":
				if model.product is None and model.outlet is None:
					views.outlet_sync(model.barcode, change, model.outlet_id)
				elif model.barcode is None and model.outlet_id is None:
					views.outlet_sync(model.product.barcode, change, model.outlet.outlet_id)
			else:
				pass
		elif isinstance(model, Product):
			outlets_with_product=RetailLink.query.filter_by(barcode=model.barcode).all()
			for outlet in outlets_with_product:
				views.outlet_sync(model.product, change, outlet.outlet)

before_models_committed.connect(outlet_db_sync, sender=app)
