from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wardrobe.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to suppress warnings
db = SQLAlchemy(app)

# Clothing item model
class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Fetch all clothing items from the database
    clothing_items = ClothingItem.query.all()
    return render_template('index.html', clothing_items=clothing_items)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        flash('Please log in to upload clothes.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        image_url = request.form['image_url']
        
        new_item = ClothingItem(name=name, image_url=image_url)
        db.session.add(new_item)
        db.session.commit()
        flash('Clothing item uploaded successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/wardrobe')
def wardrobe():
    if 'username' not in session:
        flash('Please log in to access the digital wardrobe.', 'error')
        return redirect(url_for('login'))
    
    # Fetch all clothing items from the database
    clothing_items = ClothingItem.query.all()
    return render_template('wardrobe.html', clothing_items=clothing_items)

if __name__ == '__main__':
    app.run(debug=True)
