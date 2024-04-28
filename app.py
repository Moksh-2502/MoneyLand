from flask import Flask, render_template, request, redirect, url_for, session, jsonify,abort,flash
from werkzeug.utils import secure_filename

from database_manager import init_db, add_user, get_users, get_user_by_email
from property_management import add_property, get_properties
from property_info import init_property_info_db, add_property_info, get_property_info_by_id
from feedbackmanage import add_feedback,get_feedback,init_feedback_db
import sqlite3
import os
from flask import request

app = Flask(__name__,static_folder='uploads')
app.secret_key = 'moneyland'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    users = get_users()
    return render_template('users.html', users=users)

@app.route('/register', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        add_user(name, email, phone, password)
    return render_template('home.html')

@app.route('/home', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            feedbacks = get_feedback()
            return render_template('home.html',feedbacks=feedbacks)
        else:
            return render_template('index.html', error="Incorrect email or password")

@app.route('/home')
def home():
    feedbacks = get_feedback()
    return render_template('home.html', feedbacks=feedbacks)     

@app.route('/property-maps')
def property_maps():
    properties = get_properties()
    return render_template('property_maps.html', properties=properties)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/list_properties')
def list_properties():
    return render_template('list_properties.html')


@app.route('/your_investments')
def your_investments():
    try:
        user_id = session['user_id']
        investments = get_user_investments(user_id)
        bookmarks = get_user_bookmarks(user_id)
        return render_template('your_investments.html', investments=investments, bookmarks=bookmarks)
    except KeyError:
        return "User not logged in."

def get_user_investments(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT property.idb, property.address, investment.investment FROM investment INNER JOIN property ON investment.property_id = property.idb WHERE investment.user_id = ?", (user_id,))
    investments = c.fetchall()
    conn.close()
    return investments

def get_user_bookmarks(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT bookmark.user_id, bookmark.property_id, property.address, property.price FROM bookmark INNER JOIN property ON bookmark.property_id = property.idb WHERE bookmark.user_id = ?", (user_id,))

    bookmarks = c.fetchall()
    conn.close()
    return bookmarks
def get_property_details(property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT address, price FROM property WHERE idb = ?", (property_id,))
    property_details = c.fetchone()  
    conn.close()
    return property_details


@app.route('/add-property', methods=['GET', 'POST'])
def add_property_route():
    if request.method == 'GET':
        user_id = session.get('user_id')
        
        if user_id is None:
            return redirect(url_for('login'))  
        address = request.args.get('address')
        price = float(request.args.get('price'))
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        tenure = int(request.args.get('tenure'))
        
        property_id = add_property(user_id, address, price, latitude, longitude, tenure)
        
        if property_id:
            session['property_id'] = property_id  
            return render_template('add_info.html')
        else:
            flash('Failed to add property. Please try again.', 'error')
            return redirect(url_for('error'))
@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/submit-property-info', methods=['POST'])
def submit_property_info():
    if request.method == 'POST':
        # Extract form data
        user_id = session.get('user_id')
        property_id = session.get('property_id')
        description = request.form['description']
        investing_reason = request.form['investing_reason']
        profit_scope = request.form['profit_scope']
        images = request.files.getlist('images[]')

        image_paths = []
        for image in images:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_paths.append(image_path)
        
        add_property_info(property_id, user_id, description, investing_reason, profit_scope, image_paths)

        session.pop('property_id', None)

        flash('Property information submitted successfully.', 'success')
        return render_template('listing_succesful.html')


@app.route('/give-feedback')
def give_feedback():
    return render_template('feedback.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        user_id = session.get('user_id')
        feedback_text = request.form.get('message')
        if user_id:
            add_feedback(user_id, feedback_text)
            return redirect(url_for('feedback_success'))
        else:
            return render_template('login.html', error="Please log in to leave feedback.")
    else:
        return redirect(url_for('index'))

@app.route('/thanks')
def feedback_success():
    return render_template('thanks.html')


@app.route('/get-properties')
def get_properties():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM property")
    properties = c.fetchall()
    conn.close()
    return jsonify(properties)


def get_feedbacks_with_user_names():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT feedback.message, users.name 
                 FROM feedback 
                 INNER JOIN users ON feedback.user_id = users.id''')
    feedbacks = c.fetchall()
    conn.close()
    return feedbacks

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks_api():
    feedbacks = get_feedbacks_with_user_names()
    return jsonify(feedbacks)



def get_investment_data(property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT SUM(price) FROM investment WHERE property_id = ?", (property_id,))
    total_investment = c.fetchone()[0]
    conn.close()
    return total_investment

def get_property_price(property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT price FROM property WHERE idb = ?", (property_id,))
    property_price = c.fetchone()[0]
    conn.close()
    return property_price

def calculate_remaining_amount(property_price, total_investment):
    remaining_amount = property_price - total_investment
    return remaining_amount

def get_property_info(property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT property_info.*, property.address, property.price, users.name FROM property_info JOIN property ON property_info.property_id = property.idb JOIN users ON property_info.user_id = users.id WHERE property_info.property_id = ?", (property_id,))
    property_info = c.fetchone()
    conn.close()
    return property_info

def get_property_images(property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT image_path FROM property_images WHERE property_id = ?", (property_id,))
    image_paths = c.fetchall()
    conn.close()
    return image_paths


@app.route('/investment-page', methods=['GET'])
def investment_page():
    property_id = request.args.get('property_id')
    property_info = get_property_info(property_id)
    property_price = get_property_price(property_id)
    total_investment = get_total_investment(property_id)
    remaining_amount = calculate_remaining_amount(property_price, total_investment)
    image_paths = get_property_images(property_id)  # Fetch image paths
    print(property_info)
    print(image_paths)
    if total_investment == 0:
        remaining_amount = property_price
    else:
        remaining_amount = property_price - total_investment

    return render_template('investment_page.html', property_info=property_info, property_price=property_price, total_investment=total_investment, remaining_amount=remaining_amount,image_paths=image_paths)



def get_total_investment(property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT SUM(investment) FROM investment WHERE property_id = ?", (property_id,))
    total_investment = c.fetchone()
    if total_investment and total_investment[0] is not None:
        total_investment = total_investment[0]
    else:
        total_investment = 0
    conn.close()
    return total_investment


def add_bookmark(user_id, property_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookmark (user_id, property_id) VALUES (?, ?)", (user_id, property_id))
    conn.commit()
    conn.close()

def add_investment(user_id, property_id, investment):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO investment (user_id, property_id, investment) VALUES (?, ?, ?)", (user_id, property_id, investment))
    conn.commit()
    conn.close()

@app.route('/bookmark', methods=['POST'])
def bookmark_property():
    try:
        user_id = session['user_id']
        property_id = request.form['property_id']
        add_bookmark(user_id, property_id)
        return redirect(url_for('investment_page', property_id=property_id, success=True))

    except KeyError as e:
        print("KeyError:", str(e))
        return "Error: Missing key in form data", 400
    except Exception as e:
        print("Exception:", str(e))
        return "Error: An unexpected error occurred", 500

@app.route('/invest', methods=['POST'])
def invest_property():
    try:
        user_id = session['user_id']
        property_id = request.form['property_id']
        investment = request.form['investment']
        add_investment(user_id, property_id, investment)
        return redirect(url_for('investment_page', property_id=property_id))
    except KeyError as e:
        print("KeyError:", str(e))
        return "Error: Missing key in form data", 400
    except Exception as e:
        print("Exception:", str(e))
        return "Error: An unexpected error occurred", 500

def get_user_details(user_id):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_details = c.fetchone() 
        conn.commit()  
        return user_details
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return None  
    finally:
        if conn:
            conn.close()  

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user_details = get_user_details(user_id)
        if user_details:
            return render_template('profile.html', user_details=user_details)
        else:
            return "User not found."
    else:
        return "User not logged in."
if __name__ == '__main__':
    app.run(debug=True)
