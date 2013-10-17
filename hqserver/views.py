from hqserver import app
import requests
from flask import request, make_response, jsonify, json
import simplejson
import database
@app.route('/')
def index():
	return '<a href="/admin/">Click me to get to Admin!</a>'

def outlet_sync(product_obj, db_action, outlet_obj):
	# print database.Outlet.query.get(outlet_id).outlet_server_ip
	url = (str(outlet_obj.outlet_server_ip)) + 'sync/'
	print url
	data = simplejson.dumps(product_obj.serialize(), use_decimal=True)
	headers = {'content-type': 'application/json'}
	print data
	print db_action
	if db_action=="insert":
		resp=requests.post(url, data=data, headers=headers)
		print resp.text
	elif db_action=="update":
		resp=requests.put(url, data=data, headers=headers)
		print resp.text
	elif db_action=="delete":
		resp=requests.delete(url, data=data, headers=headers)
		print resp.text

@app.route('/sync/', methods=['PUT',])
def stock_level_sync():
	if request.method=="PUT":
		data=request.get_json()
		print data
		barcode=data.get('barcode')
		max_stock=data.get('max_stock')
		min_stock=data.get('min_stock')
		outlet_ip=data.get('outlet_url')
		print outlet_ip
		outlet=database.Outlet.query.filter_by(outlet_server_ip=outlet_ip).first()
		if outlet is not None:
			retail_link=database.RetailLink.query.filter_by(barcode=barcode, outlet_id=outlet.outlet_id).first()
			if retail_link is not None:
				retail_link.product_max_stock=max_stock
				retail_link.product_min_stock=min_stock
				database.db.session.commit()
				return make_response(jsonify({'error' : 'False'}), 200)
			else:
				return make_response(jsonify({'error': 'True'}), 412)	
		else:
			return make_response(jsonify({'error': 'True'}), 403)
