from database import Products, db

product1 = Products(barcode=1234, product_name="Chandy", description="Turtle Sexpert", category="headbutt", manufacturer_name="YouTube", product_MRP="0", product_bundle_unit="0")

db.session.add(product1)
db.session.commit()