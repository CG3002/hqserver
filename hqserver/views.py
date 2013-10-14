from hqserver import app
import requests
from flask import json
import database
@app.route('/')
def index():
	return '<a href="/admin/">Click me to get to Admin!</a>'

def outlet_sync(product_barcode, db_action, outlet_id):
	product = database.Product.query.get(product_barcode)
	url = "http://" + database.Outlet.query.get(outlet_id).outlet_server_ip + "/sync/"
	data = json.dumps(product.serialize)
	print data
	print db_action
	if db_action=="insert":
		requests.post(url, data)
	elif db_action=="update":
		requests.put(url, data)
	elif db_action=="delete":
		requests.delete(url, data)

