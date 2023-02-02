from flask import redirect, render_template, session, url_for, flash, request, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please Login First','Danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database', 'Success')
        db.session.commit()
        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods = ['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please Login First','Danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'Your brand {brand.name} has been updated','Success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=["GET","POST"])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand) 
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database','Success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} can not be deleted from your database','Warning')
    return redirect(url_for('admin'))


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please Login First','Danger')
        return redirect(url_for('login'))

    if request.method == "POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        flash(f'The Category {getcat} was added to your database', 'Success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html', title= "Add category")


@app.route('/updatecat/<int:id>', methods = ['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please Login First','Danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'Your category has been updated','Success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update Category Page', updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The Category {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The Category {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))


@app.route('/addproduct', methods=["GET","POST"])
def addproduct():
    if 'email' not in session:
        flash(f'Please Login First','Danger')
        return redirect(url_for('login'))
        
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get("brand")
        category = request.form.get("category")
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")

        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc,
        brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3 )
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database','Success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', title ="Add Product Page", 
    form = form, brands = brands, categories = categories)


@app.route('/updateproduct/<int:id>', methods = ['GET', 'POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please Login First','Danger')
        return redirect(url_for('login'))
    
    brands = Brand.query.all()
    Categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)

    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.desc = form.discription.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10)+".")
        
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10)+".")
        
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10)+".")
                

        db.session.commit()
        flash(f'Your product has been updated','Success')
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc

    return render_template('products/updateproduct.html', form=form, brands=brands, Categories=Categories, product=product)


@app.route('/deleteproduct/<int:id>', methods=['GET','POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was deleted from your record','success')
        return redirect(url_for('admin'))
    flash(f'You Can not delete the product {product.name}','success')
    return redirect(url_for('admin'))