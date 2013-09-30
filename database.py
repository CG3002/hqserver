'''
This file contains the Database ORMs of the hqserver
'''
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/hari/test.db'
db = SQLAlchemy(app)

class Product(db.Model):
	__tablename__='Products'
	barcode=db.Column(db.Integer, primary_key=True)
	product_name=db.Column(db.String(32))
	description=db.Column(db.String(120))
	category=db.Column(db.String(32))
	manufacturer_name=db.Column(db.String(32))
	product_MRP=db.Column(db.Integer)
	product_bundle_unit=db.Column(db.Integer)

	def __init__(self, barcode, product_name=None, description=None, category=None, manufacturer_name=None, product_MRP=None, product_bundle_unit=0):
		self.barcode=barcode
		self.product_name=product_name
		self.description=description
		self.category=category
		self.manufacturer_name=manufacturer_name
		self.product_MRP=product_MRP
		self.product_bundle_unit=product_bundle_unit

	def __repr__(self):
		return '<Product Barcode: %r>' % self.barcode

class Outlet(db.Model):
	__tablename__='Outlets'
	outlet_id=db.Column(db.Integer, primary_key=True)
	outlet_name=db.Column(db.String(120))
	manager_name=db.Column(db.String(120))
	location=db.Column(db.String(120))

	def __init__(self, outlet_id, outlet_name=None, manager_name=None, location=None):
		self.outlet_id=outlet_id
		self.outlet_name=outlet_name
		self.manager_name=manager_name
		self.location=location

	def __repr__(self):
		return '<Outlet ID: %r>' % self.outlet_id


class RetailLink(db.Model):
	__tablename__='RetailLinks'
	barcode=db.Column(db.Integer, db.ForeignKey('Product.barcode'), primary_key=True)
	outlet_id=db.Column(db.Integer, db.ForeignKey('Outlet.outlet_id'), primary_key=True)
	product_max_stock=db.Column(db.Integer)
	product_min_stock=db.Column(db.Integer)

	def __init__(self, barcode, outlet_id, product_max_stock, product_min_stock):
		self.barcode=barcode
		self.outlet_id=outlet_id
		self.product_max_stock=product_max_stock
		self.product_min_stock=product_min_stock

	def __repr__(self):
		return '<RetailLink Barcode: %r, Outlet_ID: %r>' % (self.barcode, self.outlet_id)

class Transaction(db.Model):
	__tablename__='Transactions'
	transaction_id=db.Column(db.Integer, primary_key=True)
	outlet_id=db.Column(db.Integer, db.ForeignKey('Outlet.id'), primary_key=True)
	barcode=db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)
	cashier_id=db.Column(db.Integer)
	product_quantity=db.Column(db.Integer)
	timestamp=db.Column(db.Integer)
	outlet=db.relationship('Outlet',
        backref=db.backref('transactions', lazy='dynamic'))

	def __init__(self, transaction_id, outlet_id, barcode, cashier_id=None, product_quantity=None, timestamp=None):
		self.transaction_id=transaction_id
		self.outlet_id=outlet_id
		self.barcode=barcode
		self.cashier_id=cashier_id
		self.product_quantity=product_quantity
		if timestamp is None:
			self.timestamp=time.time()*100

	def __repr__(self):
		return '<Transaction ID: %r, Barcode: %r, Outlet ID: %r>' % (self.transaction_id, self.barcode, self.outlet_id)
