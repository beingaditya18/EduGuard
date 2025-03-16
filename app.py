from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Initialize Gemini AI API
genai.configure(api_key='AIzaSyAh3w-wr4gPCgEAyUWMXbl9ebNpRKb_jHs')

def predict_financial_aid(student):
    """Use Gemini AI to predict financial aid eligibility."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"Student details: Class {student['student_class']}, Family Income: {student['family_income']}, Parent Occupation: {student['parent_occupation']}, Digital Access: {student['digital_access']}, Distance: {student['distance']}km, Results: {student['results_percentage']}%. Provide a concise risk assessment: Alert, High Risk, Risky. Suggest what can be done."
    response = model.generate_content(prompt)
    return response.text if response else "No response from AI."

# Database model for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Database model for students
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    student_class = db.Column(db.Integer, nullable=False)
    family_income = db.Column(db.String(50), nullable=False)
    parent_occupation = db.Column(db.String(100), nullable=False)
    siblings = db.Column(db.Integer, nullable=False)
    digital_access = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    results_percentage = db.Column(db.Float, nullable=False)
    scholarship_eligibility = db.Column(db.String(10), nullable=False)

# Function to load data from Excel and insert into database
def load_student_data():
    file_path = os.path.join(os.path.dirname(__file__), 'rural_student_data_updated.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            student = Student(
                name=row['Name'],
                gender=row['Gender'],
                student_class=row['Class'],
                family_income=row['Family_Income'],
                parent_occupation=row['Parent_Occupation'],
                siblings=row['Siblings'],
                digital_access=row['Digital_Access'],
                distance=row['Distance'],
                results_percentage=row['Results_Percentage'],
                scholarship_eligibility=row['Scholarship_Eligibility']
            )
            db.session.add(student)
        db.session.commit()
    else:
        print("Error: rural_student_data_updated.xlsx file not found!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flash('Login Successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup Successful! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

@app.route('/predict/<int:student_id>')
def predict(student_id):
    student = Student.query.get_or_404(student_id)
    student_data = {
        "name": student.name,
        "student_class": student.student_class,
        "family_income": student.family_income,
        "parent_occupation": student.parent_occupation,
        "digital_access": student.digital_access,
        "distance": student.distance,
        "results_percentage": student.results_percentage
    }
    prediction = predict_financial_aid(student_data)
    return render_template('prediction.html', student=student, prediction=prediction)

@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    student_data = {
        "name": request.form['name'],
        "student_class": request.form['student_class'],
        "family_income": request.form['family_income'],
        "parent_occupation": request.form['parent_occupation'],
        "digital_access": request.form['digital_access'],
        "distance": request.form['distance'],
        "results_percentage": request.form['results_percentage']
    }
    prediction = predict_financial_aid(student_data)
    return render_template('prediction.html', student=student_data, prediction=prediction)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensures database tables are created inside the application context
        if not Student.query.first():
            load_student_data()  # Load data if database is empty
    app.run(debug=True)
