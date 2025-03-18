from flask import Blueprint, flash, session

def construct_routes(db, Item):
    from flask import render_template, redirect, url_for, request
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
    return main
