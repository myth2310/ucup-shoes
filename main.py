from flask import Flask, render_template,request, redirect,url_for

app = Flask(__name__)

database = []

@app.route('/homepage')
def homepage():
    return render_template('home-page.html')

@app.route('/aboutpage')
def aboutpage():
    return render_template('about-page.html')


@app.route('/')
def home():
    return render_template('index.html', product=database)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/about')
def about():
    name = 'Achmad Miftahudin'
    age = 16
    buah = ['apel']

    product = [
        {'name' : 'sepatu aerosreet', 'price' : 400000, 'stok' : True},
        {'name' : 'sepatu boot', 'price' : 150000, 'stok' : False},
    ]
    return render_template('about.html', myname=name, myage=age, mybuah=buah, product=product)


@app.route('/simpan-data', methods=['post'])
def submit():
    name_product = request.form['name_product'].upper()
    category = request.form['category']
    price = request.form['price']
    image_url = request.form['image_url']
    stok = request.form['stok']
    data = {
            'name' : name_product, 
            'category' : category, 
            'price' : price, 
            'image_url' : image_url,
            'stok' : stok,
            }
    database.append(data)
    return redirect(url_for('home'))