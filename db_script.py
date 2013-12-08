'''
Python script for inserting Product objects from Inventory files
'''
from hqserver import database
import codecs, time, datetime
file_object=codecs.open("hqserver/Inventory_5000.txt", 'r', 'utf-8')
# for line in file_object:
# 	line_split=line.split(':')
# 	product_name=line_split[0]
# 	category=line_split[1]
# 	manufacturer_name=line_split[2]
# 	barcode=line_split[3]
# 	product_MRP=line_split[4]
# 	product_bundle_unit=line_split[7]
# 	product=database.Product(barcode=barcode, product_name=product_name, category=category, 
# 					manufacturer_name=manufacturer_name, product_MRP=product_MRP, product_bundle_unit=product_bundle_unit)
# 	database.db.session.add(product)
# 	database.db.session.commit()

# file_object=codecs.open("Trans_50_2_9_1762.txt", 'r', 'utf-8')
# for line in file_object:
# 	line_split=line.split(':')
# 	transaction_id=line_split[0]
# 	cashier_id=line_split[1]
# 	barcode=line_split[3]
# 	quantity=line_split[4]
# 	date=line_split[5].strip()
# 	temp=time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())
# 	timestamp=temp*100
# 	new_transaction=Transaction(transaction_id=transaction_id, outlet_id=1, barcode=barcode, 
# 								cashier_id=cashier_id,product_quantity=quantity, timestamp=timestamp)
# 	db.session.add(new_transaction)
# 	db.session.commit()

# file_object=codecs.open("values_in_outlet1.txt", 'r', 'utf-8')
# for line in file_object:
# 	barcode=line
# 	outlet_id=1
# 	new_retaillink=database.RetailLink(barcode=barcode, outlet_id=outlet_id)
# 	database.db.session.add(new_retaillink)
# 	database.db.session.commit()

# file_object=codecs.open("values_in_outlet2.txt", 'r', 'utf-8')
# for line in file_object:
# 	barcode=line
# 	outlet_id=2
# 	new_retaillink=database.RetailLink(barcode=barcode, outlet_id=outlet_id)
# 	database.db.session.add(new_retaillink)
# 	database.db.session.commit()

# file_object=codecs.open("values_in_outlet3.txt", 'r', 'utf-8')
# for line in file_object:
# 	barcode=line
# 	outlet_id=3
# 	new_retaillink=database.RetailLink(barcode=barcode, outlet_id=outlet_id)
# 	database.db.session.add(new_retaillink)
# 	database.db.session.commit()

# file_object=codecs.open("values_in_outlet4.txt", 'r', 'utf-8')
# for line in file_object:
# 	barcode=line
# 	outlet_id=4
# 	new_retaillink=database.RetailLink(barcode=barcode, outlet_id=outlet_id)
# 	database.db.session.add(new_retaillink)
# 	database.db.session.commit()

file_object=codecs.open("values_in_outlet5.txt", 'r', 'utf-8')
count = 1
for line in file_object:
	barcode=line
	outlet_id=5
	new_retaillink=database.RetailLink(barcode=barcode, outlet_id=outlet_id)
	database.db.session.add(new_retaillink)
	database.db.session.commit()