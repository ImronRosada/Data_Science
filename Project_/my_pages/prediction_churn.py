import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
# import os
# st.write("Current working directory:", os.getcwd())
# st.write("Files in cwd:", os.listdir())
# Clear Streamlit cache (you can clear cache programmatically here if needed)
# Clear Streamlit cache
st.cache_data.clear()
st.cache_resource.clear()

def prediction_churn():
    st.title("Churn Prediction")
    st.info("Model Prediction using **XGBoost**")

    # Load the model and reference dataset to ensure column order
    model = joblib.load("Project_/models/xgboost_model.pkl")
    df_ref = pd.read_csv("Project_/dataset/df_churn_processed.csv")
    expected_cols = [col for col in df_ref.columns.tolist() if col != "Exited"]

    # Initialize session state to store input history
    if "history" not in st.session_state:
        st.session_state.history = []
    
    st.markdown("### Customer Data Input")
    st.info("Please fill in the data below according to the instructions.")

    row1 = st.columns(5)
    row2 = st.columns(5)
    
    # First row: 5 inputs 
    has_cr_card = row1[0].selectbox("Has Credit Card?", ["Yes", "No"], help="Select 'Yes' if the customer has a credit card.")
    credit_score = row1[1].slider("Credit Score", 300, 900, 650, help="The customer's credit score (300-900).")
    tenure = row1[2].slider("Tenure (years)", 0, 10, 5, help="How long the customer has been subscribed (in years).")
    balance = row1[3].slider("Balance", 0.0, 250000.0, 50000.0, help="The customer's account balance.")
    num_of_products = row1[4].selectbox("Number of Products", [1, 2, 3, 4], help="Number of bank products the customer has.")

    # Second row: 5 
    is_active_member = row2[0].selectbox("Is Active Member?", ["Yes", "No"], help="Select 'Yes' if the customer is active.")
    age = row2[1].slider("Age", 18, 80, 40, help="The customer's age in years.")        
    estimated_salary = row2[2].slider("Estimated Salary", 0.0, 200000.0, 50000.0, help="The customer's estimated annual salary.")
    geography = row2[3].selectbox("Geography", ["France", "Germany", "Spain"], help="The country where the customer resides.")
    gender = row2[4].selectbox("Gender", ["Female", "Male"], help="The customer's gender.")

    # Create DataFrame with raw input based on the expected order
    raw_input = pd.DataFrame({
        "HasCrCard": [1 if has_cr_card == "Yes" else 0],
        "CreditScore": [credit_score],
        "Tenure": [tenure],
        "Balance": [balance],
        "NumOfProducts": [num_of_products],
        "Age": [age],
        "IsActiveMember": [1 if is_active_member == "Yes" else 0],
        "EstimatedSalary": [estimated_salary],
        "Geography_France": [1 if geography == "France" else 0],
        "Geography_Germany": [1 if geography == "Germany" else 0],
        "Geography_Spain": [1 if geography == "Spain" else 0],
        "Gender_Female": [1 if gender == "Female" else 0],
        "Gender_Male": [1 if gender == "Male" else 0]
    })
    
    st.markdown("#### Input Data Summary")
    st.dataframe(raw_input)
    
    # Ensure all features from the training dataset are present
    for col in expected_cols:
        if col not in raw_input.columns:
            raw_input[col] = 0
    
    data = raw_input[expected_cols]

    if st.button("Predict Churn"):
        pred = model.predict(data)
        prob = model.predict_proba(data)
        churn_label = "Churn" if pred[0] == 1 else "Not Churn"
        churn_prob = round(prob[0][1] * 100, 2)
        not_churn_prob = round(prob[0][0] * 100, 2)
        
        st.subheader("Prediction Results")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### **Churn Prediction**")
            st.markdown(f'<p style="color:red;">Probability of Churn: {churn_prob}%</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"### **Not Churn Prediction**")
            st.markdown(f'<p style="color:green;">Probability of Not Churn: {not_churn_prob}%</p>', unsafe_allow_html=True)
        
        # Visualize with a Gauge Chart (Speedometer Style)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_prob,
            title={'text': "Churn Probability"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 50], 'color': "green"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "red"}
                ]
            }
        ))
        st.plotly_chart(fig)

        # Save to history with the prediction result
        raw_input["Not Churn Probability"] = not_churn_prob
        raw_input["Churn Probability"] = churn_prob
        st.session_state.history.append(raw_input)
    
    # Display input history
    st.markdown("#### Input History")
    if st.session_state.get("history"):  
        history_df = pd.concat(st.session_state.history, ignore_index=True)
    else:
        history_df = pd.DataFrame()
    if not history_df.empty:  
        st.dataframe(history_df)  
    else:
        st.info("No history available.") 

    if st.button("🔄 Reset History"):
        st.session_state.history = []
        st.rerun()

if __name__ == "__main__":
    prediction_churn()
