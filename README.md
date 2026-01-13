#  EduGuard – Financial Aid & Dropout Risk Prediction System

EduGuard is a Flask-based web application that predicts a rural student's financial aid eligibility and dropout risk using **Google Gemini AI**. It leverages socio-economic and academic features to assess vulnerability and provide personalized recommendations for improvement.

---

##  Features

-  User Signup and Login with hashed passwords (SQLAlchemy + Werkzeug)
-  Admin dashboard with student data management
-  AI-powered dropout & risk assessment using **Gemini Pro**
-  CSV-based student data upload to SQLite database
-  Recommendations for academic and social improvement

---

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS (via templates)
- **AI Model**: Google Gemini 1.5 Pro (`google.generativeai`)
- **Database**: SQLite
- **Other**: Pandas for CSV parsing, Werkzeug for password hashing

---


##  Project Structure

```
├── app.py                # Main Flask application
├── models.py             # Database models (SQLAlchemy)
├── forms.py              # WTForms for user input (optional)
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates (login, dashboard, etc.)
│   ├── login.html
│   ├── dashboard.html
│   └── ...
├── static/               # Static assets (CSS, images)
│   └── style.css
├── utils.py              # Utility functions (CSV parsing, AI integration)
├── instance/
│   └── app.sqlite        # SQLite database file
└── README.md             # Project documentation
```

---

## ⚡ Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/eduguard.git
    cd eduguard
    ```

2. **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    - Create a `.env` file for your Gemini API key and Flask secret key:
      ```
      GEMINI_API_KEY=your_google_gemini_api_key
      SECRET_KEY=your_flask_secret_key
      ```

4. **Run the application:**
    ```bash
    flask run
    ```

5. **Access the app:**  
   Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🏗️ Usage

- **Sign up** as an admin or user.
- **Upload student data** via CSV.
- **View dashboard** for AI-powered predictions and recommendations.
- **Manage student records** and monitor dropout risks.

---

## 🤖 AI Model

- Uses Google Gemini 1.5 Pro via `google.generativeai` to:
    - Analyze student socio-economic and academic data.
    - Predict financial aid eligibility and dropout risk.
    - Provide actionable recommendations.

---

## 📑 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Google Gemini](https://ai.google.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pandas](https://pandas.pydata.org/)

---
