from hqserver import app
import requests
from flask import request, make_response, jsonify, json, url_for, redirect, render_template
import simplejson
import database
import csv
from flask.ext import admin, login
from flask.ext.admin import helpers
import forms

@app.route('/')
def index():
	return render_template('index.html', user=login.current_user)

@app.route('/login/', methods=['GET', 'POST'])
def login_view():
	form = forms.LoginForm(request.form)
	if form.validate_on_submit():
		print "User password validated"
		user = form.user
		login.login_user(user)
		return redirect(url_for('index'))

	return render_template('form.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register_view():
	form = forms.RegistrationForm(request.form)
	if form.validate_on_submit():
		print "User Validate"
		user = database.User(email=form.email.data, password=form.password.data, name=form.name.data)

		database.db.session.add(user)
		database.db.session.commit()

		login.login_user(user)
		return redirect(url_for('index'))

	return render_template('form.html', form=form)

@app.route('/logout/')
def logout_view():
	login.logout_user()
	return redirect(url_for('index'))

 
def outlet_sync(product_barcode, db_action, outlet_id):
	print database.Outlet.query.get(outlet_id).outlet_server_ip
	payload = {}
	if db_action!="delete":
		produt_obj=database.Product.query.get(product_barcode)
		data = simplejson.dumps(product_obj.serialize(), use_decimal=True)
	else:
		payload['barcode'] = product_barcode
		data = simplejson.dumps(payload)
	outlet_obj=database.Outlet.query.get(outlet_id)
	url = (str(outlet_obj.outlet_server_ip)) + 'sync/'
	headers = {'content-type': 'application/json'}
	if db_action=="insert":
		resp=requests.post(url, data=data, headers=headers)
	elif db_action=="update":
		resp=requests.put(url, data=data, headers=headers)
	elif db_action=="delete":
		resp=requests.delete(url, data=data, headers=headers)
	print resp.text

@app.route('/restock', methods=['POST',])
def retail_server_restock():
	if request.method=="POST":
		return make_response(jsonify({'error' : 'False'}), 200)
	else:
		return make_response(jsonify({'error' : 'True'}), 403)

@app.route('/sync/', methods=['PUT',])
def stock_level_sync():
	if request.method=="PUT":
		data=request.get_json()
		barcode=data.get('barcode')
		max_stock=data.get('max_stock')
		min_stock=data.get('min_stock')
		outlet_ip=data.get('outlet_url')
		outlet=database.Outlet.query.filter(database.Outlet.outlet_server_ip.contains(outlet_ip)).first()
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

@app.route('/transactions/sync/', methods=['POST',])
def hq_transaction_log():
	if request.method=="POST":
		data=request.get_json()
		outlet_ip=data.get('outlet_url')
		outlet=database.Outlet.query.filter(database.Outlet.outlet_server_ip.contains(outlet_ip)).first()
		if outlet is not None:
			outlet_id = outlet.outlet_id
			products = data.get('history')
			for product in products:
				barcode=product.get('barcode')
				quantity=product.get('quantity')
				timestamp=product.get('timestamp')
				total_revenue=product.get('total_revenue')
				new_history = database.TransactionSync(barcode=barcode, outlet_id=outlet_id, quantity_sold=quantity,\
														timestamp=timestamp, total_revenue=total_revenue)
				database.db.session.add(new_history)
				database.db.session.commit()
			return make_response(jsonify({'error' : 'False'}), 200)
		else:
			return make_response(jsonify({'error': 'True'}), 403)
	# 	if outlet is not None:
	# 		try:
	# 			with open('outlet_id'+str(outlet.outlet_id)+'.csv', 'rb+') as csvfile:
	# 				has_header = csv.Sniffer().sniff(csvfile.read())
	# 		except IOError:
	# 			has_header = False
	# 		with open('outlet_id'+str(outlet.outlet_id)+'.csv', 'ab+') as csvfile:
	# 			dict_writer=csv.DictWriter(csvfile, delimiter='|', fieldnames=[u'barcode', u'quantity', u'timestamp', u'total_revenue'], extrasaction='ignore')
	# 			if has_header == False:
	# 				dict_writer.writeheader()
	# 			dict_writer.writerows(data.get('history'))
	# 		print has_header
	# 		return make_response(jsonify({'error': 'False'}), 200)
	# 	else:
	# 		return make_response(jsonify({'error': 'True'}), 403)	
	# else:
	# 	return make_response(jsonify({'error': 'True'}), 403)