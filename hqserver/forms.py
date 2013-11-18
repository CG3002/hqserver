from flask_wtf import Form
from wtforms import TextField, PasswordField, validators
import database

class LoginForm(Form):
	email = TextField(validators=[validators.required()])
	password = PasswordField(validators=[validators.required()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None

	def validate(self):
		rv = Form.validate(self)

		if not rv:
			return False

		user = database.User.query.filter_by(email=self.email.data).first()

		if user is None:
			self.email.errors.append("Unkown email")
			return False

		if not user.check_password(self.password.data):
			self.password.errors.append("Incorrect password")
			return False

		self.user = user
		return True

	# def validate_login(self, field):
	# 	print "Here"
	# 	user = self.get_user()

	# 	if user is None:
	# 		raise validators.ValidationError('Invalid User')

	# 	if not user.check_password(self.password.data):
	# 		raise validators.ValidationError('Invalid Password')

	# def get_user(self):
	# 	return database.db.session.query(database.User).filter_by(email=self.email.data).first()

class RegistrationForm(Form):
	email = TextField(validators=[validators.required()])
	password = PasswordField(validators=[validators.required()])
	name = TextField(validators=[validators.required()])

	def validate(self):
		rv = Form.validate(self)

		if not rv:
			return False

		user_count = database.User.query.filter_by(email=self.email.data).count()

		if user_count > 0:
			self.email.errors.append("Email already exists")
			return False

		return True


