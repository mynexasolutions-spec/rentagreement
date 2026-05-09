from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import functools

app = Flask(__name__)
app.secret_key = 'pune-online-agreement-secret-key-2025' # Change this in production

# Supabase PostgreSQL Configuration
# Password URL-encoded: @ -> %40
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.xuxmidhrmnvvzjxeqnuz:Nexasolutions%400302@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Authentication Decorator
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Database Model
class FormEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    type = db.Column(db.String(50))
    city = db.Column(db.String(50))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables within app context
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/online-form')
def online_form():
    return render_template('form.html')

@app.route('/fee-calculator')
def fee_calculator():
    return render_template('calculator.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    try:
        new_entry = FormEntry(
            name=data.get('name') or data.get('owner_name'),
            phone=data.get('phone') or data.get('owner_phone'),
            type=data.get('type') or data.get('agreement_type'),
            city=data.get('city'),
            message=data.get('message') or data.get('special_terms')
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Form submitted successfully! Our team will contact you shortly.'})
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'status': 'error', 'message': 'Internal server error. Please call us directly.'}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Using a simple hardcoded password for now
        if request.form.get('password') == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    entries = FormEntry.query.order_by(FormEntry.created_at.desc()).all()
    return render_template('admin.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
