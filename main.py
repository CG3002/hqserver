from hqserver import app
from hqserver.database import db, Product, RetailLink, Outlet
from flask.ext.admin import Admin
from hqserver.model_views import ProductAdmin, OutletAdmin, RetailLinkAdmin

admin = Admin(app, name="HQ Server")

# Add views
admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(RetailLinkAdmin(RetailLink, db.session))
admin.add_view(OutletAdmin(Outlet, db.session))
# admin.add_view(sqlamodel.ModelView(Post, session=db.session))

# Create DB
db.create_all()


if __name__ == '__main__':
    # Create admin
    # Start app
    app.debug = True
    app.run('127.0.0.1', 5000)