from flask import Flask, render_template,request, redirect,url_for,jsonify,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'Ucup Store'

# Konfigurasi Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'web1_3e'

mysql = MySQL(app)

@app.route('/cek_database')
def cekDatabase():
    cur = mysql.connection.cursor()
    cur.execute('SELECT 1')
    return jsonify({'message' : 'Database Berhasil terkoneksi'})

database = [
    {'name': 'sepatu compas', 'price': 15000,'stok':True ,'image_url': 'https://www.static-src.com/wcsstore/Indraprastha/images/catalog/full//catalog-image/100/MTA-118564740/compass_sepatu_compass_gazelle_low_-_wafer_green_full01_c50196ea.jpg'},
    {'name': 'sepatu aerostreet', 'price': 50000,'stok':True ,'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2NN9NoBXlzTMT-CN6wjKZrDkVfvToY_n8Y-XCEVlekIh14jBiE-xW2nzqZmH2nc_P7ps&usqp=CAU'},
]

@app.route('/')
def home():
    return render_template('index.html',product=database)

@app.route('/aboutpage')
def aboutpage():
    return render_template('about-page.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/simpan-data', methods=['post'])
def submit():
    name_product = request.form['name_product'].upper()
    category = request.form['category']
    price = request.form['price']
    data = {
            'name' : name_product, 
            'category' : category, 
            'price' : price, 
            }
    database.append(data)
    return redirect(url_for('home'))

@app.route('/about')
def about():
    name = 'Eka'
    age = 15
    buah = ['apel','duren','semangka']

    product = [
        {'name' : 'sabun', 'price' : 1000, 'stok' : True},
        {'name' : 'molto', 'price' : 1000, 'stok' : False},
    ]
    return render_template('about.html', myname=name, myage=age, buah=buah,product=product)

@app.route('/product')
def product():
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM product'
    cur.execute(query)
    product = cur.fetchall()
    return jsonify(product)

@app.route('/homepage')
def homepage():
    cur = mysql.connection.cursor()
    # query = 'SELECT * FROM product'
    query = ''' SELECT product.*, category.name_category FROM product
                INNER JOIN category
                ON product.category = category.id_category
            '''
    cur.execute(query)
    product = cur.fetchall()
    # return jsonify(product)
    return render_template('home-page.html',product=product)

@app.route('/form-product')
def form_add_product():
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM category'
    cur.execute(query)
    category = cur.fetchall()
    return render_template('form-product.html', category=category)

@app.route('/add-product', methods=['post'])
def add_product():
    # Request data dari form
    name_product = request.form['name_product']
    image_url = request.form['image_url']
    price = request.form['price']
    category = request.form['category']
    in_stok = request.form['in_stok']

    # Validasi Data
    if not name_product:
        flash('Name product harus diisi','error')
        return redirect('/homepage')

    # Query Menyimpan ke tabel
    cur = mysql.connection.cursor()
    query = ''' INSERT INTO product(name_product,image_url,price,category,in_stok) 
                VALUES (%s, %s, %s, %s,%s)
            '''
    cur.execute(query, (name_product, image_url, price, category, in_stok))
    mysql.connection.commit()

    flash('Data Berhasil disimpan','success')
    return redirect('/homepage')


@app.route('/form-edit-product/<int:id>')
def form_edit_product(id):
    cur = mysql.connection.cursor()
    query = 'SELECT * FROM product WHERE id = %s'
    cur.execute(query,[id])
    product = cur.fetchone()

    query = 'SELECT * FROM category'
    cur.execute(query)
    category = cur.fetchall()
    # return jsonify(product)
    return render_template('form-edit-product.html', product=product, category=category)

@app.route('/edit-product/<int:id>', methods=['post'])
def edit_product(id):
    # Request data dari form
    name_product = request.form['name_product']
    image_url = request.form['image_url']
    price = request.form['price']
    category = request.form['category']
    in_stok = request.form['in_stok']

    # Query Menyimpan ke tabel
    cur = mysql.connection.cursor()
    query = ''' UPDATE product SET
                name_product = %s,
                image_url = %s,
                price = %s,
                category = %s,
                in_stok = %s
                WHERE id = %s
            '''
    cur.execute(query, (name_product, image_url, price, category, in_stok, id))
    mysql.connection.commit()
    flash('Data Berhasil diedit','success')
    return redirect('/homepage')

@app.route('/delete-product/<int:id>', methods=['get'])
def delete_product(id):
    cur = mysql.connection.cursor()
    query = 'DELETE FROM product WHERE id = %s'
    cur.execute(query,[id])
    mysql.connection.commit()
    flash('Data berhasil dihapus','success')
    return redirect('/homepage')