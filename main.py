from flask import Flask, render_template,request, redirect,url_for,jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'Ucup Store'

# Konfigurasi Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'web1_3d'

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
    return render_template('form-product.html')

@app.route('/add-product', methods=['POST'])
def add_product():
    # Request data dari form
    name_product = request.form['name_product']
    image_url = request.form['image_url']
    price = request.form['price']
    category = request.form['category']
    in_stok = request.form['in_stok']

    # Menyimpan data ke tabel
    cur = mysql.connection.cursor()
    query = 'INSERT INTO product VALUES (%s, %s, %s, %s, %s)'
    cur.execute(query,(name_product, image_url, price, category, in_stok))
    mysql.connection.commit()

    return 
