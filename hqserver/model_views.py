'''
This file contains the Model Views for Flask admin
'''
from flask.ext.admin.contrib import sqla

class ProductAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['barcode', 'product_name', 'description', 'category', 
					'manufacturer_name', 'product_MRP', 'product_bundle_unit']

class OutletAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['outlet_id', 'outlet_name', 'manager_name', 'location', 'outlet_server_ip']

class RetailLinkAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['outlet', 'product', 'product_max_stock', 'product_min_stock']



