'''
This file contains the Model Views for Flask admin
'''
from flask.ext.admin.contrib import sqla
import database
from flask.ext.admin.contrib.sqla.filters import *
from flask.ext import admin, login

class ProductAdmin(sqla.ModelView):
	column_display_pk = True
	column_filters = ('barcode', )
	column_searchable_list = ('product_name', database.Product.product_name)
	form_columns = ['barcode', 'product_name', 'description', 'category', 
					'manufacturer_name', 'product_MRP', 'product_bundle_unit']

	def is_accessible(self):
		if login.current_user.is_authenticated():
			print login.current_user
			print login.current_user.user_id
			print login.current_user.is_administrator()
			return login.current_user.is_administrator()
		else: 
			return False


class OutletAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['outlet_id', 'outlet_name', 'manager_name', 'location', 'outlet_server_ip']

	def is_accessible(self):
		if login.current_user.is_authenticated():
			return login.current_user.is_administrator()
		else:
			return False

class RetailLinkAdmin(sqla.ModelView):
	column_display_pk = True
	can_edit = False
	column_filters = ('barcode', 'outlet_id')
	form_columns = ['outlet', 'product']

	def is_accessible(self):
		if login.current_user.is_authenticated():
			return login.current_user.is_administrator()
		else:
			return False

class TransactionHistory(sqla.ModelView):
	column_display_pk = True
	can_edit = True
	column_filters = ('barcode', 'outlet_id', 'timestamp')

	def is_accessible(self):
		if login.current_user.is_authenticated():
			return login.current_user.is_administrator()
		else:
			return False


