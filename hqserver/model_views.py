'''
This file contains the Model Views for Flask admin
'''
from flask.ext.admin.contrib import sqla
import database
from flask.ext.admin.contrib.sqla.filters import *

class ProductAdmin(sqla.ModelView):
	column_display_pk = True
	column_filters = ('barcode', )
	column_searchable_list = ('product_name', database.Product.product_name)
	form_columns = ['barcode', 'product_name', 'description', 'category', 
					'manufacturer_name', 'product_MRP', 'product_bundle_unit']


class OutletAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['outlet_id', 'outlet_name', 'manager_name', 'location', 'outlet_server_ip']

class RetailLinkAdmin(sqla.ModelView):
	column_display_pk = True
	can_edit = False
	column_filters = ('barcode', 'outlet_id')
	form_columns = ['outlet', 'product']



