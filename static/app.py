from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
import pandas as pd
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = ''  # Replace 'your_secret_key' with a strong, random key!
db = SQLAlchemy(app)

# Initialize Gemini AI API
genai.configure(api_key='')  # Replace with your actual Gemini API key!

def predict_financial_aid(student):
    """Use Gemini AI to predict financial aid eligibility."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""Student details: 
        Class: {student['student_class']}, 
        Family Income: {student['family_income']}, 
        Parent Occupation: {student['parent_occupation']}, 
        Digital Access: {student['digital_access']}, 
        Distance: {student['distance']}km, 
        Results: {student['results_percentage']}%.
        Provide a concise risk assessment: Alert, High Risk, Risky. Suggest improvements."""
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            text = response.text.split("Suggested Improvements:")
            risk_assessment = text[0].strip()
            improvements = text[1].strip() if len(text) > 1 else "No improvements suggested."
            return {
                "risk": risk_assessment,
                "recommendation": improvements,
                "financial_risk": "Analyzing...",
                "dropout_probability": "Analyzing...",
                "recommendations": improvements
            }
        else:
            return {
                "risk": "No response from AI.",
                "recommendation": "No AI insights available.",
                "financial_risk": "Analyzing...",
                "dropout_probability": "Analyzing...",
                "recommendations": "No recommendations."
            }
    except Exception as e:
        print(f"Error during AI prediction: {e}")
        return {
            "risk": "AI prediction failed.",
            "recommendation": "AI prediction failed.",
            "financial_risk": "Analyzing...",
            "dropout_probability": "Analyzing...",
            "recommendations": "No recommendations."
        }


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

# Function to load data from CSV and insert into database
def load_student_data():
    file_path = os.path.join(os.path.dirname(__file__), 'rural_student_data_cleaned.csv')
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            student = Student(
                name=row['Name'],
                gender=row['Gender'],
                student_class=row['Class'],
                family_income=row['Family Income'],
                parent_occupation=row.get("Parent's Occupation", "Unknown"),
                siblings=row['Number of Siblings'],
                digital_access=row['Access to Digital Resources'],
                distance=row['Distance from School (km)'],
                results_percentage=row['Results in Percentage'],
                scholarship_eligibility=row['Scholarship Eligibility']
            )
            db.session.add(student)
        db.session.commit()
    else:
        print("Error: rural_student_data_cleaned.csv file not found!")

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

@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    student_data = {
        "name": request.form.get('name', ''),
        "student_class": request.form.get('student_class', ''),
        "family_income": request.form.get('family_income', ''),
        "parent_occupation": request.form.get('parent_occupation', ''),
        "digital_access": request.form.get('digital_access', ''),
        "distance": request.form.get('distance', '0'),
        "results_percentage": request.form.get('results_percentage', '0')
    }
    prediction = predict_financial_aid(student_data)
    return render_template('prediction.html', student=student_data, prediction=prediction)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Student.query.first():
            load_student_data()
    app.run(debug=True)
