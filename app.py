from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date, time

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ehoh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yoursecretkey'  # Change this to a secure secret key

# Initialize the database
db = SQLAlchemy(app)

# Define the Client model
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    ssn = db.Column(db.String(12), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    height = db.Column(db.String(10))
    weight = db.Column(db.String(10))
    eye_color = db.Column(db.String(50))
    hair_color = db.Column(db.String(50))

    # Relationships
    appointments = db.relationship('Appointment', backref='client', lazy=True)
    medications = db.relationship('Medication', backref='client', lazy=True)
    awol_reports = db.relationship('AWOLReport', backref='client', lazy=True)
    behaviors = db.relationship('Behavior', backref='client', lazy=True)

# Define the Doctor model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))

    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

# Define the Appointment model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(200))

# Define the Medication model
class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    prescribing_doctor = db.Column(db.String(100))

# Define the AWOL Report model
class AWOLReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    summary = db.Column(db.String(500))

# Define the Behavior model
class Behavior(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(500))

# Define the Staff model
class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    clients = Client.query.all()
    return render_template('dashboard.html', clients=clients)

# Route for the clients page
@app.route('/clients')
def clients():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    all_clients = Client.query.all()
    return render_template('clients.html', clients=all_clients)

# Route to edit a client
@app.route('/edit_client/<int:client_id>', methods=['GET', 'POST'])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == 'POST':
        client.first_name = request.form['first_name']
        client.last_name = request.form['last_name']
        client.ssn = request.form['ssn']
        client.dob = request.form['dob']
        client.height = request.form['height']
        client.weight = request.form['weight']
        client.eye_color = request.form['eye_color']
        client.hair_color = request.form['hair_color']
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template('edit_client.html', client=client)

# Route to delete a client
@app.route('/delete_client/<int:client_id>', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for('clients'))

# Route for the doctors page
@app.route('/doctors')
def doctors():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

# Route to edit a doctor
@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    if request.method == 'POST':
        doctor.name = request.form['name']
        doctor.specialty = request.form['specialty']
        doctor.phone = request.form['phone']
        doctor.address = request.form['address']
        db.session.commit()
        return redirect(url_for('doctors'))
    return render_template('edit_doctor.html', doctor=doctor)

# Route to delete a doctor
@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('doctors'))

# Route for the medications page
@app.route('/medications')
def medications():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    medications = Medication.query.all()
    return render_template('medications.html', medications=medications)

# Route to edit a medication
@app.route('/edit_medication/<int:medication_id>', methods=['GET', 'POST'])
def edit_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    if request.method == 'POST':
        medication.name = request.form['name']
        medication.dosage = request.form['dosage']
        medication.frequency = request.form['frequency']
        medication.prescribing_doctor = request.form['prescribing_doctor']
        db.session.commit()
        return redirect(url_for('medications'))
    return render_template('edit_medication.html', medication=medication)

# Route to delete a medication
@app.route('/delete_medication/<int:medication_id>', methods=['POST'])
def delete_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    db.session.delete(medication)
    db.session.commit()
    return redirect(url_for('medications'))

# Route for the AWOL reports page
@app.route('/awol')
def awol():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    awols = AWOLReport.query.all()
    return render_template('awol.html', awols=awols)

# Route to edit an AWOL report
@app.route('/edit_awol/<int:awol_id>', methods=['GET', 'POST'])
def edit_awol(awol_id):
    awol = AWOLReport.query.get_or_404(awol_id)
    if request.method == 'POST':
        awol.date = request.form['date']
        awol.time = request.form['time']
        awol.summary = request.form['summary']
        db.session.commit()
        return redirect(url_for('awol'))
    return render_template('edit_awol.html', awol=awol)

# Route to delete an AWOL report
@app.route('/delete_awol/<int:awol_id>', methods=['POST'])
def delete_awol(awol_id):
    awol = AWOLReport.query.get_or_404(awol_id)
    db.session.delete(awol)
    db.session.commit()
    return redirect(url_for('awol'))

# Route for the behavior reports page
@app.route('/behavior')
def behavior():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    behaviors = Behavior.query.all()
    return render_template('behavior.html', behaviors=behaviors)

# Route to edit a behavior report
@app.route('/edit_behavior/<int:behavior_id>', methods=['GET', 'POST'])
def edit_behavior(behavior_id):
    behavior = Behavior.query.get_or_404(behavior_id)
    if request.method == 'POST':
        behavior.date = request.form['date']
        behavior.time = request.form['time']
        behavior.description = request.form['description']
        db.session.commit()
        return redirect(url_for('behavior'))
    return render_template('edit_behavior.html', behavior=behavior)

# Route to delete a behavior report
@app.route('/delete_behavior/<int:behavior_id>', methods=['POST'])
def delete_behavior(behavior_id):
    behavior = Behavior.query.get_or_404(behavior_id)
    db.session.delete(behavior)
    db.session.commit()
    return redirect(url_for('behavior'))

# Route for the staff page
@app.route('/staff')
def staff():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    staff = Staff.query.all()
    return render_template('staff.html', staff=staff)

# Route to edit a staff member
@app.route('/edit_staff/<int:staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    if request.method == 'POST':
        staff.first_name = request.form['first_name']
        staff.last_name = request.form['last_name']
        staff.email = request.form['email']
        staff.employee_id = request.form['employee_id']
        db.session.commit()
        return redirect(url_for('staff'))
    return render_template('edit_staff.html', staff=staff)

# Route to delete a staff member
@app.route('/delete_staff/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    db.session.delete(staff)
    db.session.commit()
    return redirect(url_for('staff'))

# Route for the search page
@app.route('/search')
def search():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('search.html')

# Route for the settings page
@app.route('/settings')
def settings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('settings.html')

# Route for the upload page
@app.route('/upload')
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('upload.html')

# Route for the contacts page
@app.route('/contacts')
def contacts():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('contacts.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
