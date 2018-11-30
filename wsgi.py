# wsgi.py
try:
    from dotenv import load_dot_env
    load_dotenv()
except:
    pass

from flask import Flask, request, Response, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

from models import Product
from schemas import products_schema, product_schema

@app.route('/')
def hello():
    products = db.session.query(Product).all()
    return render_template('home.html', products=products)

@app.route('/product/<int:id>', methods=['GET'])
def product(id):
    product = db.session.query(Product).get(id)
    return render_template('products.html', product=product)

@app.route('/api/v1/products',methods = ['GET','POST'])
def products():
    if request.method == 'GET':
        products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
        return products_schema.jsonify(products)
    elif request.method == 'POST':
        content = request.get_json()
        new_product = Product()
        new_product.name = content['name']
        new_product.description = content['description']
        db.session.add(new_product)
        db.session.commit()
        return Response(f"added {content['name']} with desription {content['description']}", status=201, mimetype='application/json')

@app.route('/api/v1/products/<int:id>',methods = ['GET','DELETE','PATCH'])
def get_product(id):
    if request.method == 'GET':
        single_product = db.session.query(Product).get(id)
        return product_schema.jsonify(single_product)
    elif request.method == 'PATCH':
        content = request.get_json()
        product = db.session.query(Product).get(id)
        if product:
            if content['name'] != '':
                product.name = content['name']
            if content['description'] != '':
                product.description = content['description']
            db.session.commit()
            return Response(None, status=204, mimetype='application/json')
        content = {'error unknown id': ''}
        return Response(content, status=404, mimetype='application/json')
    elif request.method == 'DELETE':
        product = db.session.query(Product).get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return Response('', status=204, mimetype='application/json')
        content = {'error unknown id': ''}
        return Response(content, status=404, mimetype='application/json')
