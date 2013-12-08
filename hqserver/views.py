from hqserver import app
import requests
from flask import request, make_response, jsonify, json, url_for, redirect, render_template, g
import simplejson
import database
import csv
from flask.ext import admin, login
from flask.ext.admin import helpers
import forms

@app.route('/')
def index():
	# trolleys=None
	# if g.user.is_authenticated() is True:
	# 	trolleys=database.TrolleyLink.query.filter_by(user_id=g.user.user_id).all()
	# 	print trolleys
	# return render_template('index.html', user=g.user, trolleys=trolleys)
	outlets=None
	if g.user.is_authenticated() is True:
		outlets=database.Outlet.query.all()
		print outlets
	return render_template('index.html', user=g.user, outlets=outlets)

@login.login_required
@app.route('/outlet/<outlet_id>/')
def outlet_view(outlet_id=None):
	trolleys=database.TrolleyLink.query.filter_by(user_id=g.user.user_id).all()
	print trolleys
	return render_template('outlet.html', user=g.user, trolleys=trolleys, outlet_id=outlet_id)

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

@app.route('/products/search/<outlet_id>/', methods=['GET', ])
def autocomplete_search(outlet_id):
	term=request.args.get('term')
	data = []
	if outlet_id is not None:
		for barcode, name, category in database.db.session.query(database.RetailLink.barcode, \
										database.Product.product_name, database.Product.category).\
										filter(database.Product.barcode==database.RetailLink.barcode).\
										filter(database.RetailLink.outlet_id==outlet_id).\
										filter(database.Product.product_name.ilike(term+"%")).\
										order_by(database.Product.category).all():
			data.append({'label': name, 'category': category, 'id' : barcode})
		print json.dumps(data)
		return make_response(json.dumps(data), 200, {'content-type': 'application/json'})
	else:
		return make_response(json.dumps(data), 200, {'content-type': 'application/json'})


@app.route('/logout/')
@login.login_required
def logout_view():
	login.logout_user()
	return redirect(url_for('index'))

@app.before_request
def before_request():
	g.user = login.current_user

@app.route('/trolley/<outlet_id>/')
@app.route('/trolley/<trolley_id>/<outlet_id>')
@login.login_required
def trolley_view(trolley_id=None, outlet_id=None):
	if trolley_id is None:
		items=None
	else:
		items=database.db.session.query(database.Trolley.trolley_id, \
									database.Product.product_name, \
									database.Trolley.barcode, \
									database.Trolley.quantity).\
									join(database.Product).\
									filter(database.Product.barcode==database.Trolley.barcode).\
									filter(database.Trolley.trolley_id==trolley_id).all()
		print items
	return render_template('trolley.html', user=g.user, trolley_items=items, trolley_id=trolley_id, outlet_id=outlet_id)


@app.route('/validate/', methods=['GET'])
def validate_barcode():
	barcode=request.args.get('barcode', None)
	quantity=request.args.get('quantity', None)
	print barcode
	print quantity
	product_obj=database.Product.query.get(int(barcode))
	if product_obj is None:
		return make_response(jsonify({'error': 'Barcode does not exist'}), 200)
	return make_response(jsonify({'success': 'True'}), 200)

@app.route('/validate/<outlet_id>/quantity/<barcode>/', methods=['GET', 'POST'])
def validate_quantity(outlet_id, barcode):
	outlet = database.Outlet.query.get(outlet_id)
	if outlet is not None:
		quantity=request.args.get('quantity')
		outlet_server_ip=str(outlet.outlet_server_ip)+"quantity/validate/"+str(barcode)
		payload={'quantity' : quantity}
		print outlet_server_ip
		# return make_response(jsonify({'error': 'Server Error'}), 200)
		resp = requests.get(url=outlet_server_ip, params=payload)
		print resp.json()
		print resp.status_code
		print resp.headers
		return make_response(jsonify(resp.json()), 200)
	else:
		return make_response(jsonify({'error': 'Server Error'}), 200)

@app.route('/trolley/create/', methods=['POST', ])
def trolley_data():
 	data = request.get_json()
 	barcodes = data.get('barcode')
 	quantities = data.get('quantity')
 	trolley_id = data.get('trolley_id', None)
 	flag=True
 	print barcodes
 	print quantities
 	trolley=[]
 	if type(barcodes).__name__=='list':
	 	for barcode, quantity in zip(barcodes, quantities):
	 		trolley.append({'barcode' : barcode, 'quantity' : quantity })
	else:
	 	trolley.append({'barcode' : barcodes, 'quantity' : quantities})
	if trolley_id is None: 
		new_trolley=database.TrolleyLink(user_id=g.user.user_id)
		database.db.session.add(new_trolley)
		database.db.session.commit()
		flag=database.Trolley.create_trolley(trolley=trolley, trolley_id=new_trolley.trolley_id)
	else:
		print trolley_id
		database.Trolley.query.filter(database.Trolley.trolley_id==trolley_id).delete()
		database.TrolleyLink.query.filter(database.TrolleyLink.trolley_id==trolley_id).delete()
		new_trolley=database.TrolleyLink(user_id=g.user.user_id, trolley_id=trolley_id)
		database.db.session.add(new_trolley)
		database.db.session.commit()
		flag=database.Trolley.create_trolley(trolley=trolley, trolley_id=new_trolley.trolley_id)
	if flag == False:
		return make_response(jsonify({'error': 'True'}), 500)
 	return make_response(jsonify({'success': 'True'}), 200)

@app.route('/trolley/<trolley_id>/delete/', methods=['POST'])
@login.login_required
def delete_trolley(trolley_id=None):
	if trolley_id is None:
		return make_response(jsonify({'status': "Trolley doesn't exist"}), 200)
	else:
		database.Trolley.query.filter(database.Trolley.trolley_id==trolley_id).delete()
		database.TrolleyLink.query.filter(database.TrolleyLink.trolley_id==trolley_id).delete()
		database.db.session.commit()
		return make_response(jsonify({'status': "Trolley deleted"}), 200)

@app.route('/get/trolley/', methods=['POST'])
def return_trolley():
	data=request.get_json()
	trolley_id=data.get('trolley')
	print trolley_id
	trolleys=database.Trolley.query.filter_by(trolley_id=trolley_id).all()
	payload = []
	if trolleys is None:
		error_payload={'error': True}
		return make_response(json.dumps(error_payload), 200, {'content-type': 'application/json'})
	for trolley in trolleys:
		payload.append({'barcode': trolley.barcode, 'quantity': trolley.quantity})
		print payload
	return make_response(json.dumps(payload), 200, {'content-type': 'application/json'})

@app.route('/get/price/', methods=['POST'])
def return_trolley_price():
	outlet_id=request.get_json().get('outlet_id')
	trolley_id=request.get_json().get('trolley_id')
	outlet = database.Outlet.query.get(outlet_id)
	trolleys=database.Trolley.query.filter_by(trolley_id=trolley_id).all()
	payload = []
	if trolleys is None:
		error_payload={'error': True}
		return make_response(json.dumps(error_payload), 200, {'content-type': 'application/json'})
	outlet_ip=str(outlet.outlet_server_ip)+"get/price/"
	for trolley in trolleys:
		payload.append({'barcode': trolley.barcode, 'quantity': trolley.quantity})
	headers = {'content-type' : 'application/json'}
	resp=requests.post(outlet_ip, data=json.dumps(payload), headers=headers)
	return make_response(jsonify(resp.json()), 200)	

@app.route('/product/name/', methods=['POST'])
def return_product_name():
	data=request.get_json()
	barcode=data.get('barcode')
	product=database.Product.query.get(barcode)
	if product is not None:
		return make_response(jsonify({'product_name': product.product_name}), 200)
	return make_response(jsonify({'product_name': "Product doesn't Exist"}), 200)

def outlet_sync(product_barcode, db_action, outlet_id):
	print database.Outlet.query.get(outlet_id).outlet_server_ip
	payload = {}
	if db_action!="delete":
		product_obj=database.Product.query.get(int(product_barcode))
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

@app.route('/restock/', methods=['POST',])
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