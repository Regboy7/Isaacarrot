from flask import Blueprint, render_template, redirect, url_for, request
from app import db
from app.models import Item

main = Blueprint('main', __name__)

@main.route('/')
def home():
    items = Item.query.all()
    return render_template('home.html', items=items)

@main.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name')
    description = request.form.get('description')
    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.home'))
