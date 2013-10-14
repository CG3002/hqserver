from hqserver import app
from flask.ext.superadmin import Admin, model
from hqserver.database import db, Product, RetailLink, Outlet, Transaction

if __name__ == '__main__':
    # Create admin
    admin = Admin(app, 'HQ Server Admin')

    # Add views
    admin.register(Product, session=db.session)
    admin.register(Outlet, session=db.session)
    admin.register(RetailLink, session=db.session)
    admin.register(Transaction, session=db.session)
    # admin.add_view(sqlamodel.ModelView(Post, session=db.session))

    # Create DB
    db.create_all()

    # Start app
    app.debug = True
    app.run('127.0.0.1', 8000)