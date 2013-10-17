from hqserver import app
import requests
from flask import json
import database
@app.route('/')
def index():
	return '<a href="/admin/">Click me to get to Admin!</a>'

def outlet_sync(product_obj, db_action, outlet_obj):
	# print database.Outlet.query.get(outlet_id).outlet_server_ip
	url = (str(outlet_obj.outlet_server_ip)) + '/sync/'
	print url
	data = json.dumps(product_obj.serialize)
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