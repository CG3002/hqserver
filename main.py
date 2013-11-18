from hqserver import app
from hqserver.database import db, Product, RetailLink, Outlet, TransactionSync, User
from flask.ext.admin import Admin
from hqserver.model_views import ProductAdmin, OutletAdmin, RetailLinkAdmin, TransactionHistory
from flask.ext import login

admin = Admin(app, name="HQ Server")

# Add views
admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(RetailLinkAdmin(RetailLink, db.session))
admin.add_view(OutletAdmin(Outlet, db.session))
admin.add_view(TransactionHistory(TransactionSync, db.session))
# admin.add_view(sqlamodel.ModelView(Post, session=db.session))

# Create DB
db.create_all()

#Initialize login
def init_login():
	login_manager=login.LoginManager()
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		return db.session.query(User).get(user_id)

if __name__ == '__main__':
    # Create admin
    # Start app
    init_login()
    app.debug = True
    app.run('0.0.0.0', 8000)