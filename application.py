from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Cricketer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jersey_number = db.Column(db.Integer, nullable=False)
    player = db.Column(db.String(100), nullable=False)

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jersey_number = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    cricketers = Cricketer.query.all()
    countries = Country.query.all()
    return render_template('index.html', cricketers=cricketers, countries=countries)

# Cricketer CRUD operations

@app.route('/add_cricketer', methods=['POST'])
def add_cricketer():
    jersey_number = request.form['jersey_number']
    player = request.form['player']
    new_cricketer = Cricketer(jersey_number=jersey_number, player=player)
    db.session.add(new_cricketer)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_cricketer/<int:id>', methods=['GET', 'POST'])
def edit_cricketer(id):
    cricketer = Cricketer.query.get(id)
    if request.method == 'POST':
        cricketer.jersey_number = request.form['jersey_number']
        cricketer.player = request.form['player']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_cricketer.html', cricketer=cricketer)

@app.route('/delete_cricketer/<int:id>')
def delete_cricketer(id):
    cricketer = Cricketer.query.get(id)
    db.session.delete(cricketer)
    db.session.commit()
    return redirect(url_for('index'))

# Country CRUD operations

@app.route('/add_country', methods=['POST'])
def add_country():
    jersey_number = request.form['jersey_number']
    country = request.form['country']
    new_country = Country(jersey_number=jersey_number, country=country)
    db.session.add(new_country)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit_country/<int:id>', methods=['GET', 'POST'])
def edit_country(id):
    country = Country.query.get(id)
    if request.method == 'POST':
        country.jersey_number = request.form['jersey_number']
        country.country = request.form['country']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_country.html', country=country)

@app.route('/delete_country/<int:id>')
def delete_country(id):
    country = Country.query.get(id)
    db.session.delete(country)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
