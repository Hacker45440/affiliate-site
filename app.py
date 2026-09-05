from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Product
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///affiliate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

ADMIN_PASSWORD = "soumen454"  # Eta apni change korben

# ---------- Public routes ----------
@app.route('/')
def home():
    category = request.args.get('category', '')
    if category:
        products = Product.query.filter_by(is_active=True, category=category).all()
    else:
        products = Product.query.filter_by(is_active=True).all()
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    return render_template('index.html', products=products, categories=categories, selected_category=category)

# ---------- Admin login ----------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Wrong password!')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

def check_admin():
    return session.get('is_admin', False)

# ---------- Admin dashboard ----------
@app.route('/admin')
def admin_dashboard():
    if not check_admin():
        return redirect(url_for('admin_login'))
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add():
    if not check_admin():
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            price=request.form['price'],
            image_url=request.form['image_url'],
            platform=request.form['platform'],
            affiliate_link=request.form['affiliate_link'],
            category=request.form.get('category', 'General')
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_add.html')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit(id):
    if not check_admin():
        return redirect(url_for('admin_login'))
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.image_url = request.form['image_url']
        product.platform = request.form['platform']
        product.affiliate_link = request.form['affiliate_link']
        product.category = request.form.get('category', 'General')
        product.is_active = 'is_active' in request.form
        db.session.commit()
        flash('Product updated!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', product=product)

@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    if not check_admin():
        return redirect(url_for('admin_login'))
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
