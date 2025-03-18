from flask import Blueprint, flash, session
from flask import Blueprint, request, jsonify
from app.forms import RegisterForm 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def construct_routes(db, Item, User):
    from flask import render_template, redirect, url_for, request
    main = Blueprint('main', __name__)


    @main.route('/')
    def home():
        items = Item.query.all()
        return render_template('home.html', items=items)

    @main.route('/add_item', methods=['GET', 'POST'])
    def add_item():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            new_item = Item(name=name, description=description)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!', 'success')
            return redirect(url_for('main.home'))
    
        return render_template('add_item.html')


    @main.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials', 'danger')

        return render_template('login.html')

    @main.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('Logged out successfully', 'info')
        return redirect(url_for('login'))

    @main.route('/update/<int:id>', methods=['GET', 'POST'])
    def update_item(id):
        item = Item.query.get_or_404(id)
        if request.method == 'POST':
            item.name = request.form['name']
            item.description = request.form['description']
            db.session.commit()
            flash('Item updated successfully', 'success')
            return redirect(url_for('home'))

        return render_template('update_item.html', item=item)

    @main.route('/delete/<int:id>', methods=['POST'])
    def delete_item(id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully', 'danger')
        return redirect(url_for('home'))

    @main.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():  # Checks if form is valid
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)
    return main