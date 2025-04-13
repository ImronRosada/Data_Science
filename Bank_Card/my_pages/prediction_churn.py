import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

st.cache_data.clear()
st.cache_resource.clear()

def app():
    st.title("📈 Churn Prediction - Bank Credit Card")
    st.info("Prediction model using **XGBoost** or **SVM** based on credit card customer data.")

    model_option = st.radio("Select Model", ["XGBoost", "SVM"], horizontal=True, help="Choose a prediction model to use.")
    model_path = "Bank_Card/models/xgb_model.pkl" if model_option == "XGBoost" else "Bank_Card/models/svm_model.pkl"
    model = joblib.load(model_path)

    if model_option == "XGBoost":
        with st.expander("ℹ️ XGBoost Model Performance"):
            st.markdown("""
            This model achieved a high accuracy of **96%** on the test set.  

            | Class      | Confusion Matrix       | Precision | Recall | F1-score |
            |------------|------------------------|-----------|--------|----------|
            | Not Churn  | TN [827] | FP [31]     | 0.99      | 0.96   | 0.98     |
            | Churn      | FN [11]  | TP [144]    | 0.82      | 0.93   | 0.87     |
            """)

            st.markdown("##### Feature Importance and Shapley Additive Explanations (SHAP) - XGBoost")
            col1, col2 = st.columns(2)
            with col1:
                st.image(Image.open("Bank_Card/img/output1.png"), caption="Top Features", use_container_width=True)
            with col2:
                st.image(Image.open("Bank_Card/img/output3.png"), caption="SHAP Summary Plot", use_container_width=True)

    else:
        with st.expander("ℹ️ SVM Model Performance"):
            st.markdown("""
            This model achieved an accuracy of **93%** on the test set.  

            | Class      | Confusion Matrix       | Precision | Recall | F1-score |
            |------------|------------------------|-----------|--------|----------|
            | Not Churn  | TN [822] | FP [36]     | 0.96      | 0.96   | 0.96     |
            | Churn      | FN [35]  | TP [120]    | 0.77      | 0.77   | 0.77     |
            """)

            st.markdown("##### Feature Importance and Shapley Additive Explanations (SHAP) - SVM")
            col1, col2 = st.columns(2)
            with col1:
                st.image(Image.open("Bank_Card/img/output2.png"), caption="Top Features", use_container_width=True)
            with col2:
                st.image(Image.open("Bank_Card/img/output4.png"), caption="SHAP Summary Plot", use_container_width=True)

    df_ref = pd.read_csv("Bank_Card/dataset/df_churn_test_scaled.csv")
    expected_cols = [col for col in df_ref.columns if col != "Attrition_Flag"]

    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown("#### Customer Form")

    row1 = st.columns(4)
    row2 = st.columns(4)
    row3 = st.columns(4)
    row4 = st.columns(4)

    age = row1[0].slider("Customer Age", 26, 73, 40, help="Customer's age in years.")
    gender = row1[1].selectbox("Gender", ["M", "F"], help="Customer's gender.")
    dependents = row1[2].slider("Number of Dependents", 0, 5, 1, help="Number of dependents the customer has.")
    total_rel = row1[3].slider("Total Relationship Count", 1, 6, 3, help="Total number of products/services used.")

    months_inactive = row2[0].slider("Months Inactive (Last 12 Months)", 0, 6, 2, help="Months the customer was inactive.")
    contacts = row2[1].slider("Contact Count (Last 12 Months)", 0, 6, 2, help="Times bank contacted the customer.")
    credit_limit = row2[2].slider("Credit Limit", 1438.0, 34516.0, 10000.0, help="Credit limit available.")
    total_revolving = row2[3].slider("Total Revolving Balance", 0.0, 2517.0, 800.0, help="Unpaid revolving balance.")

    amt_chg = row3[0].slider("Total Amount Change (Q4/Q1)", 0.0, 3.397, 1.2, help="Change in amount from Q1 to Q4.")
    ct_chg = row3[1].slider("Transaction Count Change (Q4/Q1)", 0.0, 3.714, 0.8, help="Change in count from Q1 to Q4.")    
    trans_amt = row3[2].slider("Total Transaction Amount", 510.0, 18484.0, 5000.0, help="Total transaction amount.")
    trans_ct = row3[3].slider("Total Transaction Count", 10, 139, 60, help="Total number of transactions.")

    util_ratio = row4[0].slider("Utilization Ratio", 0.0, 0.999, 0.3, help="Credit utilization ratio.")

    education = row4[1].selectbox("Education Level", [
        "College", "Graduate", "High School", "Post-Graduate", "Uneducated", "Unknown"
    ], help="Highest education level.")

    marital = row4[2].selectbox("Marital Status", [
        "Divorced", "Married", "Single", "Unknown"
    ], help="Marital status of the customer.")

    income = row4[3].selectbox("Income Category", [
        "$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K", "Unknown"
    ], help="Annual income category.")

    # Construct feature dictionary
    raw_input = {
        "Customer_Age": age,
        "Gender": 1 if gender == "F" else 0,
        "Dependent_count": dependents,
        "Total_Relationship_Count": total_rel,
        "Months_Inactive_12_mon": months_inactive,
        "Contacts_Count_12_mon": contacts,
        "Credit_Limit": credit_limit,
        "Total_Revolving_Bal": total_revolving,
        "Total_Amt_Chng_Q4_Q1": amt_chg,
        "Total_Trans_Amt": trans_amt,
        "Total_Trans_Ct": trans_ct,
        "Total_Ct_Chng_Q4_Q1": ct_chg,
        "Avg_Utilization_Ratio": util_ratio,
    }

    for level in ["College", "Graduate", "High School", "Post-Graduate", "Uneducated", "Unknown"]:
        raw_input[f"Education_Level_{level}"] = 1 if education == level else 0

    for status in ["Divorced", "Married", "Single", "Unknown"]:
        raw_input[f"Marital_Status_{status}"] = 1 if marital == status else 0

    for inc in ["$120K +", "$40K - $60K", "$60K - $80K", "$80K - $120K", "Less than $40K", "Unknown"]:
        raw_input[f"Income_Category_{inc}"] = 1 if income == inc else 0

    input_df = pd.DataFrame([raw_input])

    with st.expander("📋 Input Summary"):
        st.dataframe(input_df)

    for col in expected_cols:
        if col not in input_df.columns:
            input_df[col] = 0
    data = input_df[expected_cols]

    if st.button("Predict Churn"):
        pred = model.predict(data)
        prob = model.predict_proba(data)
        label = "Attrited (Churn)" if pred[0] == 1 else "Existing (Not Churn)"
        churn_prob = round(prob[0][1] * 100, 2)
        not_churn_prob = round(prob[0][0] * 100, 2)

        st.warning(f"**Prediction Result:** {label}")

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.markdown("#### Churn Probability")
            st.markdown(f"<h3 style='color:red; font-weight:bold;'>{churn_prob:.2f}%</h3>", unsafe_allow_html=True)
        with col2:
            st.markdown("#### Not Churn Probability")
            st.markdown(f"<h3 style='color:green; font-weight:bold;'>{not_churn_prob:.2f}%</h3>", unsafe_allow_html=True)
        with col3:
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
            fig.update_layout(height=150, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)

        input_df["Churn Probability"] = churn_prob
        input_df["Not Churn Probability"] = not_churn_prob
        st.session_state.history.append(input_df)

    st.markdown("#### History Data")
    if st.session_state.history:
        hist_df = pd.concat(st.session_state.history, ignore_index=True)
        st.dataframe(hist_df)
    else:
        st.info("No input history available.")

    if st.button("Reset History"):
        st.session_state.history = []
        st.rerun()

if __name__ == "__main__":
    app()
