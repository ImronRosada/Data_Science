import streamlit as st

def app():
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>Customer Retention Insights</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 25px; border-radius: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.05); font-size: 16px;">
            <h4 style="color: #3b82f6;">Model Comparison Summary</h4>
            <p>This section highlights key features identified by XGBoost and SVM models in predicting customer churn, along with practical business recommendations to improve customer retention.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Feature Insights by Model")
        st.markdown("""
        | **Category**               | **XGBoost**                                                                                         | **SVM**                                                                                              | **Conclusion**                                                                                                                |
        |---------------------------|------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
        | **Churn Retention Features** | Total_Trans_Ct, Total_Trans_Amt, Total_Relationship_Count, Total_Revolving_Bal                     | Total_Trans_Ct, Total_Trans_Amt, Total_Revolving_Bal, Total_Ct_Chng_Q4_Q1                            | Transaction frequency and value reflect loyalty. In SVM, changes in transaction count (Total_Ct_Chng_Q4_Q1) also indicate retention. |
        | **Churn Trigger Features**   | Total_Amt_Chng_Q4_Q1, Months_Inactive_12_mon, Contacts_Count_12_mon, Credit_Limit                   | Months_Inactive_12_mon, Contacts_Count_12_mon, Customer_Age, Avg_Utilization_Ratio                   | Changes in transaction patterns and reduced interaction (e.g., increased inactive months and fewer contacts) signal churn potential. |
        | **Non-influential Features** | Education_Level_Unknown, Education_Level_Graduate, Income_Category_Unknown                           | Income_Category_Unknown, Education_Level_Post-Graduate                                               | Education and income category variables tend to have minimal impact on churn in both models.                                       |
        | **Negative Features**        | Marital_Status_Single, Education_Level_High School, Income_Category_Less than 40K<br>(features with higher negative SHAP values in XGBoost) | Education_Level_Graduate, Income_Category_Less than 40K, Income_Category_60K - 80K<br>(dominant negative values indicate churn risk) | Negative values indicate that increases in these features (related to demographics or certain interaction aspects) are linked to churn risk. |
        | **Model Differences**        | Emphasizes transaction volume and value as loyalty indicators.                                      | Focuses more on behavioral dynamics (e.g., transaction changes) and inactivity duration.              | XGBoost focuses on quantitative transactional aspects, while SVM captures behavioral changes over time.                          |
        | **Feature Relationship to Churn** | Customers with consistent transactions and strong relationships tend to show higher loyalty.     | Fluctuating transaction patterns, especially with inactivity or fewer contacts, tend to increase churn risk. | Active customer engagement is key to retention; significant behavior shifts may lead to churn.                                    |
        """, unsafe_allow_html=True)

        st.markdown("#### 💡 Business Recommendations")
        st.markdown("""
        | **Business Recommendation**                        | **Action**                                                                                                                                                                                                                                                  |
        |----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
        | **Encourage Transaction Frequency and Value**      | - Increase **Total_Trans_Ct** and **Total_Trans_Amt** through loyalty programs, cashback, or special discounts.<br> - Motivate customers to transact more often with exclusive offers and scheduled promotions.                                             |
        | **Expand Customer Relationships**                  | - Boost **Total_Relationship_Count** by offering more products or services per customer.<br> - Implement personalized **cross-selling** and **upselling** strategies to strengthen loyalty.                                                                |
        | **Balance Revolving Balances**                     | - Monitor **Total_Revolving_Bal** to avoid high revolving balances.<br> - Adjust **Credit_Limit** strategically to remain competitive and match customer capacity.<br> - Provide financial education to improve retention.                                 |
        | **Re-activate Passive Customers**                  | - Focus on **Months_Inactive_12_mon** and **Contacts_Count_12_mon** to identify inactive customers.<br> - Use re-engagement tactics like transaction reminders, special offers, or personal consultations.                                                  |
        | **Monitor Behavioral Pattern Changes**             | - Track **Total_Ct_Chng_Q4_Q1** and **Total_Amt_Chng_Q4_Q1** to detect significant shifts in transaction behavior.<br> - Implement early warning systems and automated interventions for customers with unstable transaction patterns.                      |
        | **Address Risks Based on Customer Profiles**       | - Be aware of certain age segments using the **Customer_Age** feature.<br> - Assess **Avg_Utilization_Ratio** to identify potential financial risks that could lead to churn.                                                                              |
        | **Focus Strategy on Customer Behavior**            | - Since **Income_Category_Unknown**, **Income_Category_80K - 120K**, **Education_Level_Unknown**, **Education_Level_Post-Graduate**, **Education_Level_Uneducated**, and **Education_Level_College** show little or negative impact, focus on behavior patterns.<br> - Prioritize customer engagement over demographic data. |
        """, unsafe_allow_html=True)
