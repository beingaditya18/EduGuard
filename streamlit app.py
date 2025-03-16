import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# Initialize Gemini AI API
genai.configure(api_key='AIzaSyAh3w-wr4gPCgEAyUWMXbl9ebNpRKb_jHs')

def predict_financial_aid(student):
    """Use Gemini AI to predict financial aid eligibility."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"Student details: Class {student['student_class']}, Family Income: {student['family_income']}, Parent Occupation: {student['parent_occupation']}, Digital Access: {student['digital_access']}, Distance: {student['distance']}km, Results: {student['results_percentage']}%. Provide a concise risk assessment: Alert, High Risk, Risky. Suggest what can be done."
    response = model.generate_content(prompt)
    return response.text if response else "No response from AI."

# Load student data from Excel
def load_student_data():
    file_path = os.path.join(os.path.dirname(__file__), 'rural_student_data_updated.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return df
    else:
        st.error("Error: rural_student_data_updated.xlsx file not found!")
        return None

# Main Streamlit app
def main():
    st.title("Financial Aid Prediction")

    df = load_student_data()
    if df is None:
        return

    # Display student data
    st.subheader("Student Data")
    st.dataframe(df)

    # Prediction for selected student
    st.subheader("Predict Financial Aid")
    selected_student_id = st.selectbox("Select Student ID", df['ID'].tolist())
    selected_student = df[df['ID'] == selected_student_id].iloc[0]

    if st.button("Predict"):
        student_data = {
            "student_class": selected_student['Class'],
            "family_income": selected_student['Family_Income'],
            "parent_occupation": selected_student['Parent_Occupation'],
            "digital_access": selected_student['Digital_Access'],
            "distance": selected_student['Distance'],
            "results_percentage": selected_student['Results_Percentage']
        }
        prediction = predict_financial_aid(student_data)
        st.write("Prediction:", prediction)

    # Manual prediction
    st.subheader("Manual Prediction")
    name = st.text_input("Name")
    student_class = st.number_input("Class", min_value=1, max_value=12, value=1)
    family_income = st.text_input("Family Income")
    parent_occupation = st.text_input("Parent Occupation")
    digital_access = st.text_input("Digital Access")
    distance = st.number_input("Distance (km)", min_value=0, value=0)
    results_percentage = st.number_input("Results Percentage", min_value=0.0, max_value=100.0, value=0.0)

    if st.button("Predict Manual"):
        student_data = {
            "student_class": student_class,
            "family_income": family_income,
            "parent_occupation": parent_occupation,
            "digital_access": digital_access,
            "distance": distance,
            "results_percentage": results_percentage
        }
        prediction = predict_financial_aid(student_data)
        st.write("Prediction:", prediction)

if __name__ == "__main__":
    main()