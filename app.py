from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from datetime import datetime
import functools
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pune-online-agreement-secret-key-2025')
Compress(app) # Enable Gzip compression

# Supabase PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres.xuxmidhrmnvvzjxeqnuz:Nexasolutions%400302@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres')
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
    
    # New detailed fields
    owner_aadhaar = db.Column(db.String(20))
    owner_pan = db.Column(db.String(20))
    tenant_name = db.Column(db.String(100))
    tenant_phone = db.Column(db.String(20))
    property_address = db.Column(db.Text)
    rent = db.Column(db.String(20))
    deposit = db.Column(db.String(20))
    start_date = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    
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
            name=data.get('owner_name') or data.get('name'),
            phone=data.get('owner_phone') or data.get('phone'),
            type=data.get('agreement_type') or data.get('type'),
            city=data.get('city'),
            message=data.get('special_terms') or data.get('message'),
            
            # New mapping
            owner_aadhaar=data.get('owner_aadhaar'),
            owner_pan=data.get('owner_pan'),
            tenant_name=data.get('tenant_name'),
            tenant_phone=data.get('tenant_phone'),
            property_address=data.get('property_address'),
            rent=data.get('rent'),
            deposit=data.get('deposit'),
            start_date=data.get('start_date'),
            duration=data.get('duration')
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
        if request.form.get('password') == 'Nexasolutions@0302':
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
    try:
        entries = FormEntry.query.order_by(FormEntry.created_at.desc()).all()
        return render_template('admin.html', entries=entries)
    except Exception as e:
        # If column is missing, try to auto-update
        if 'UndefinedColumn' in str(e) or 'no such column' in str(e):
            return redirect(url_for('update_db'))
        raise e

@app.after_request
def add_header(response):
    # Cache static files for 1 year
    if request.path.startswith('/static/'):
        response.cache_control.max_age = 31536000
    return response

@app.route('/admin/update-db')
@login_required
def update_db():
    try:
        from sqlalchemy import text
        # Add missing columns one by one
        columns = [
            ("owner_aadhaar", "VARCHAR(20)"),
            ("owner_pan", "VARCHAR(20)"),
            ("tenant_name", "VARCHAR(100)"),
            ("tenant_phone", "VARCHAR(20)"),
            ("property_address", "TEXT"),
            ("rent", "VARCHAR(20)"),
            ("deposit", "VARCHAR(20)"),
            ("start_date", "VARCHAR(50)"),
            ("duration", "VARCHAR(50)")
        ]
        
        for col_name, col_type in columns:
            try:
                db.session.execute(text(f"ALTER TABLE form_entry ADD COLUMN {col_name} {col_type}"))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Column {col_name} might already exist: {e}")
        
        return "Database updated successfully! <a href='/admin'>Go back to Dashboard</a>"
    except Exception as e:
        return f"Error updating database: {e}"

@app.route('/admin/delete/<int:id>', methods=['POST'])
@login_required
def delete_entry(id):
    entry = FormEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
