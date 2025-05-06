import streamlit as st

def app():
    st.markdown("<h2 style='text-align: center; color: #3b82f6;'>Delivery Operation Time Insights</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        This section highlights model performance metrics from Random Forest and XGBoost in predicting delivery time and classifying delivery speed, along with practical recommendations to improve delivery operations.
        """)

        st.markdown("#### Summary")
        st.markdown("""
        | **Task**                                    | **Model**    | **Metric** | **Value**    | **Interpretation**                            |
        | ------------------------------------------- | ------------ | ---------- | ------------ | --------------------------------------------- |
        | ⏱️ Delivery Time Estimation                 | RandomForest | MAE        | 3.33 minutes | More accurate and stable predictions          |
        |    (Regression)                             |              | R²         | 0.80         | Higher R², indicating better fit              |
        |                                             | XGBoost      | MAE        | 4.43 minutes | Slightly less accurate predictions            |
        |                                             |              | R²         | 0.61         | Lower R², indicating less optimal performance |
        | 🛵️ Slow Delivery Detection                 | RandomForest | Accuracy   | 93.3%        | High accuracy                                 |
        |    (Classification)                         |              | Recall     | 0.86         | Lower recall compared to XGBoost              |
        |                                             |              | Precision  | 0.94         | Slightly higher precision than XGBoost        |
        |                                             | XGBoost      | Accuracy   | 92.7%        | High accuracy                                 |
        |                                             |              | Recall     | 0.91         | Better at detecting slow deliveries           |
        |                                             |              | Precision  | 0.93         | Slightly lower precision than RandomForest    |
        """, unsafe_allow_html=True)

        st.markdown("#### 💡 Business Recommendations")
        st.markdown("""
        | **Recommendation**                                                                                                                                                                                             |
        | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
        | Use RandomForest for ETA **(Estimated Time of Arrival)** System, RandomForest provides more accurate predictions with smaller errors and explains 80% of the variation in delivery duration.                       |
        | Use XGBoost for **Slow Delivery Detection**, XGBoost minimizes the risk of missing delayed packages due to its higher recall.                                                                                      |
        | Evaluate Model Performance Periodically, Perform monthly evaluations of both models (using **MAE, R², and recall**) to ensure consistent performance.                                                              |
        | Integrate Results into **Real-Time Dashboard**, Integrate the results into a real-time operation dashboard, allowing the team to take proactive actions such as customer notifications or rescheduling deliveries. |
        """, unsafe_allow_html=True)