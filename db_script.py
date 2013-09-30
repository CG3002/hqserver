'''
Python script for inserting Product objects from Inventory files
'''

from database import Product, db
import codecs
file_object=codecs.open("Inventory_100.txt", 'r', 'utf-8')
for line in file_object:
	line_split=line.split(':')
	product_name=line_split[0]
	category=line_split[1]
	manufacturer_name=line_split[2]
	barcode=line_split[3]
	product_MRP=line_split[4]
	product_bundle_unit=line_split[7]
	product=Product(barcode=barcode, product_name=product_name, category=category, 
					manufacturer_name=manufacturer_name, product_MRP=product_MRP, product_bundle_unit=product_bundle_unit)
	db.session.add(product)
	db.session.commit()
