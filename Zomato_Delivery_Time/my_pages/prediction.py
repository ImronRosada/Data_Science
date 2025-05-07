import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# Clear cache (optional during development)
st.cache_data.clear()
st.cache_resource.clear()

def app():
    st.title("⏱️ Delivery Time - 🛵️ Delivery Speed Prediction")
    st.info("Prediction models using **Random Forest** and **XGBoost** to estimate delivery time and classify delivery speed.")

    tab_reg, tab_cls = st.tabs(["⏱️ Regression", "🛵️ Classification"])

    # === Regression Tab ===
    with tab_reg:
        st.subheader("⏱️ Regression")
        # Model selection for regression
        reg_model_option = st.radio("Select Model", ["Random Forest", "XGBoost"], horizontal=True, help="Choose a prediction model to use.", key="reg_model_option")
        reg_model_path = ("Zomato_Delivery_Time/models/rf_reg_model.pkl" if reg_model_option == "Random Forest" else "Zomato_Delivery_Time/models/xgb_reg_model.pkl")
        reg_model = joblib.load(reg_model_path)

        # === Performance Info ===
        if reg_model_option == "Random Forest":
            with st.expander("ℹ️ Random Forest Performance"):
                st.markdown("""
                This model achieved an R² of **80%** on the test set.

                | Metric    | Value            |
                |-----------|------------------|
                | MAE       | 3.33 minutes     |
                | RMSE      | 4.18 minutes     |
                | MAPE      | 14.68%           |
                | R² Score  | 0.80 (80%)       |
                """)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(Image.open("Zomato_Delivery_Time/img/rf_fi_reg.png"), caption="Top Features", use_container_width=True)
                with col2:
                    st.image(Image.open("Zomato_Delivery_Time/img/rf_SHAP_reg.png"), caption="SHAP Summary Plot", use_container_width=True)
        else:
            with st.expander("ℹ️ XGBoost Performance"):
                st.markdown("""
                This model achieved an R² of **61%** on the test set.

                | Metric    | Value            |
                |-----------|------------------|
                | MAE       | 4.43 minutes     |
                | RMSE      | 5.80 minutes     |
                | MAPE      | 20.20%           |
                | R² Score  | 0.61 (61%)       |
                """)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(Image.open("Zomato_Delivery_Time/img/xg_fi_reg.png"), caption="Top Features", use_container_width=True)
                with col2:
                    st.image(Image.open("Zomato_Delivery_Time/img/xg_SHAP_reg.png"), caption="SHAP Summary Plot", use_container_width=True)

        # Reference columns (exclude target)
        df_ref_reg = pd.read_csv("Zomato_Delivery_Time/dataset/df_zomato_test_reg.csv")
        expected_cols_reg = [ col for col in df_ref_reg.columns  if col not in ("Time_taken (min)", "delivery_time")]

        # Input form for regression
        st.markdown("#### Form Delivery Time")
        row1 = st.columns(4)
        row2 = st.columns(4)
        row3 = st.columns(4)
        row4 = st.columns(4)

        # Tambahkan key unik dengan suffix _reg
        age_reg = row1[0].slider("Delivery Person Age", 15, 50, 30, help="Delivery person's age.", key='age_reg')
        ratings_reg = row1[1].slider("Delivery Person Ratings", 0.0, 6.0, 4.5, help="Delivery person rating.", key='ratings_reg')
        vehicle_condition_reg = row1[2].slider("Vehicle Condition", 0, 3, 1, help="Condition of the vehicle.", key='vehicle_reg')
        multiple_deliveries_reg = row1[3].selectbox("Multiple Deliveries", [0, 1, 2, 3], help="If multiple deliveries are happening in a single trip.", key='multi_reg')

        day_of_week_reg = row2[0].selectbox("Day of the Week", list(range(7)), help="Day of the week for the delivery.", key='dow_reg')
        hour_of_day_reg = row2[1].slider("Hour of the Day", 0, 23, 12, help="Hour at which delivery is made.", key='hour_reg')
        waiting_time_reg = row2[2].slider("Waiting Time (minutes)", 10.0, 60.0, 26.0, 1.0, help="Waiting time before delivery.", key='wait_reg')
        distance_km_reg = row2[3].slider("Delivery Distance (km)", 1.5, 30.0, 10.0, 0.1, help="Distance to the delivery address.", key='dist_reg')

        traffic_density_reg = row3[0].selectbox("Traffic Density", [0, 1, 2, 3], help="Traffic density during delivery (0=Low, 1=Medium, 2=High, 3=Very High).", key='traffic_reg')
        weather_condition_reg = row3[1].selectbox("Weather Condition", ["Fog", "Sandstorms", "Stormy", "Sunny", "Windy"], help="Weather condition.", key='weather_reg')
        road_traffic_density_reg = row3[2].selectbox("Road Traffic Density", ["Medium", "Very High"], help="Road traffic density.", key='road_reg')
        type_of_order_reg = row3[3].selectbox("Type of Order", ["Drinks", "Meal", "Snack"], help="Type of order for delivery.", key='order_reg')

        vehicle_type_reg = row4[0].selectbox("Type of Vehicle", ["Electric Scooter", "Motorcycle"], help="Type of vehicle used for delivery.", key='vehicle_type_reg')
        city_type_reg = row4[1].selectbox("City Type", ["Urban"], help="The type of city where delivery occurs.", key='city_reg')

        # Construct feature dictionary
        raw_input_reg = {
            "Delivery_person_Age": age_reg,
            "Delivery_person_Ratings": ratings_reg,
            "Vehicle_condition": vehicle_condition_reg,
            "multiple_deliveries": multiple_deliveries_reg,
            "day_of_week": day_of_week_reg,
            "hour_of_day": hour_of_day_reg,
            "waiting_time": waiting_time_reg,
            "distance_km": distance_km_reg,
            "traffic_density_score": traffic_density_reg,
        }

        # One-hot encoding manual (dataset sudah ter-encoding)
        for weather in ["Fog", "Sandstorms", "Stormy", "Sunny", "Windy"]:
            raw_input_reg[f"Weather_conditions_{weather}"] = 1 if weather_condition_reg == weather else 0

        for traffic in ["Medium", "Very High"]:
            raw_input_reg[f"Road_traffic_density_{traffic}"] = 1 if road_traffic_density_reg == traffic else 0

        for order in ["Drinks", "Meal", "Snack"]:
            raw_input_reg[f"Type_of_order_{order}"] = 1 if type_of_order_reg == order else 0

        for vehicle in ["electric_scooter", "motorcycle"]:
            raw_input_reg[f"Type_of_vehicle_{vehicle}"] = 1 if vehicle_type_reg.lower().replace(" ", "_") == vehicle else 0

        for city in ["Urban"]:
            raw_input_reg[f"City_{city}"] = 1 if city_type_reg == city else 0

        input_df_reg = pd.DataFrame([raw_input_reg])
        input_df_reg = input_df_reg.reindex(columns=expected_cols_reg, fill_value=0)

        # Show input summary
        with st.expander("📋 Input Summary (Regression)"):
            st.dataframe(input_df_reg)

        if "history_reg" not in st.session_state:
            st.session_state.history_reg = []

        if st.button("Predict Delivery Time", key='predict_reg'):
            try:
                pred_time = reg_model.predict(input_df_reg)[0]

                if pred_time > 30:
                    st.error(f"**Estimated Delivery Time: {pred_time:.2f} minutes**")
                else:
                    st.success(f"**Estimated Delivery Time: {pred_time:.2f} minutes**")

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("#### Estimated Time")
                    st.markdown(f"<h3 style='color: orange; font-weight:bold;'>{pred_time:.2f} minutes</h3>", 
                                unsafe_allow_html=True)
                with col2:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=pred_time,
                        title={'text': "Predicted Delivery Time"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "orange"},
                            'steps': [
                                {'range': [0, 50], 'color': "green"},
                                {'range': [50, 75], 'color': "yellow"},
                                {'range': [75, 100], 'color': "red"}
                            ]
                        }
                    ))
                    fig.update_layout(height=150, margin=dict(t=10, b=10, l=10, r=10))
                    st.plotly_chart(fig, use_container_width=True)

                input_df_reg["Predicted Delivery Time (min)"] = pred_time
                st.session_state.history_reg.append(input_df_reg)

            except Exception as e:
                st.error(f"Prediction failed: {e}")

        st.markdown("#### Regression History")
        if st.session_state.history_reg:
            hist_df_reg = pd.concat(st.session_state.history_reg, ignore_index=True)
            st.dataframe(hist_df_reg)
        else:
            st.info("No regression history available.")

        # Tombol reset history
        if st.button("Reset History", key='reset_reg'):
            st.session_state.history_reg = []
            st.rerun()

    # === Classification Tab ===
    with tab_cls:
        st.subheader("🛵️ Classification")
        model_option_clas = st.radio("Select Model", ["Random Forest", "XGBoost"], horizontal=True, help="Choose a prediction model to use.", key="model_option_clas")
        model_path_clas = "Zomato_Delivery_Time/models/rf_class_model.pkl" if model_option_clas == "Random Forest" else "Zomato_Delivery_Time/models/xgb_class_model.pkl"
        model_clas = joblib.load(model_path_clas)

        # Model Performance
        if model_option_clas == "Random Forest":
            with st.expander("ℹ️ Random Forest Model Performance"):
                st.markdown("""
                This model achieved a high accuracy of **93%** on the test set.  

                | Class      | Confusion Matrix       | Precision | Recall | F1-score |
                |------------|------------------------|-----------|--------|----------|
                | Fast       | TN [3081]  FP [118]    | 0.94      | 0.96   | 0.95     |
                | Slow       | FN [185]   TP [1175]   | 0.91      | 0.86   | 0.89     |
                """)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(Image.open("Zomato_Delivery_Time/img/rf_fi_class.png"), caption="Top Features", use_container_width=True)
                with col2:
                    st.image(Image.open("Zomato_Delivery_Time/img/rf_SHAP_class.png"), caption="SHAP Summary Plot", use_container_width=True)
        else:
            with st.expander("ℹ️ XGBoost Model Performance"):
                st.markdown("""
                This model achieved an accuracy of **92%** on the test set.  

                | Class      | Confusion Matrix       | Precision | Recall | F1-score |
                |------------|------------------------|-----------|--------|----------|
                | Fast       | TN [2991]  FP [208]    | 0.96      | 0.93   | 0.95     |
                | Slow       | FN [122]   TP [1238]   | 0.86      | 0.91   | 0.88     |
                """)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(Image.open("Zomato_Delivery_Time/img/xg_fi_class.png"), caption="Top Features", use_container_width=True)
                with col2:
                    st.image(Image.open("Zomato_Delivery_Time/img/xg_SHAP_class.png"), caption="SHAP Summary Plot", use_container_width=True)

        # Input Form
        df_ref_clas = pd.read_csv("Zomato_Delivery_Time/dataset/df_zomato_test_clas.csv")
        expected_cols_clas = [col for col in df_ref_clas.columns if col != "delivery_speed_category"]

        if "history_clas" not in st.session_state:
            st.session_state.history_clas = []

        st.markdown("#### Form Delivery Speed")

        row1_clas = st.columns(4)
        row2_clas = st.columns(4)
        row3_clas = st.columns(4)
        row4_clas = st.columns(4)

        # Input fields dengan suffix _clas
        age_clas = row1_clas[0].slider("Delivery Person Age", 15, 50, 30, help="Delivery person's age.", key='age_clas')
        ratings_clas = row1_clas[1].slider("Delivery Person Ratings", 0.0, 6.0, 4.5, help="Delivery person rating.", key='ratings_clas')
        vehicle_condition_clas = row1_clas[2].slider("Vehicle Condition", 0, 3, 1, help="Condition of the vehicle.", key='vehicle_clas')
        multiple_deliveries_clas = row1_clas[3].selectbox("Multiple Deliveries", [0, 1, 2, 3], help="If multiple deliveries are happening in a single trip.", key='multi_clas')

        day_of_week_clas = row2_clas[0].selectbox("Day of the Week", list(range(7)), help="Day of the week for the delivery.", key='dow_clas')
        hour_of_day_clas = row2_clas[1].slider("Hour of the Day", 0, 23, 12, help="Hour at which delivery is made.", key='hour_clas')
        waiting_time_clas = row2_clas[2].slider("Waiting Time (minutes)", 10.0, 60.0, 26.0, 1.0, help="Waiting time before delivery.", key='wait_clas')
        distance_km_clas = row2_clas[3].slider("Delivery Distance (km)", 1.5, 30.0, 10.0, 0.1, help="Distance to the delivery address.", key='dist_clas')

        traffic_density_clas = row3_clas[0].selectbox("Traffic Density", [0, 1, 2, 3], help="Traffic density during delivery (0=Low, 1=Medium, 2=High, 3=Very High).", key='traffic_clas')
        weather_condition_clas = row3_clas[1].selectbox("Weather Condition", ["Fog", "Sandstorms", "Stormy", "Sunny", "Windy"], help="Weather condition.", key='weather_clas')
        road_traffic_density_clas = row3_clas[2].selectbox("Road Traffic Density", ["Medium", "Very High"], help="Road traffic density.", key='road_clas')
        type_of_order_clas = row3_clas[3].selectbox("Type of Order", ["Drinks", "Meal", "Snack"], help="Type of order for delivery.", key='order_clas')

        vehicle_type_clas = row4_clas[0].selectbox("Type of Vehicle", ["Electric Scooter", "Motorcycle"], help="Type of vehicle used for delivery.", key='vehicle_type_clas')
        city_type_clas = row4_clas[1].selectbox("City Type", ["Urban"], help="The type of city where delivery occurs.", key='city_clas')

        # Construct feature dictionary
        raw_input_clas = {
            "Delivery_person_Age": age_clas,
            "Delivery_person_Ratings": ratings_clas,
            "Vehicle_condition": vehicle_condition_clas,
            "multiple_deliveries": multiple_deliveries_clas,
            "day_of_week": day_of_week_clas,
            "hour_of_day": hour_of_day_clas,
            "waiting_time": waiting_time_clas,
            "distance_km": distance_km_clas,
            "traffic_density_score": traffic_density_clas,
        }

        # One-hot encoding manual (dataset sudah ter-encoding)
        for weather in ["Fog", "Sandstorms", "Stormy", "Sunny", "Windy"]:
            raw_input_clas[f"Weather_conditions_{weather}"] = 1 if weather_condition_clas == weather else 0

        for traffic in ["Medium", "Very High"]:
            raw_input_clas[f"Road_traffic_density_{traffic}"] = 1 if road_traffic_density_clas == traffic else 0

        for order in ["Drinks", "Meal", "Snack"]:
            raw_input_clas[f"Type_of_order_{order}"] = 1 if type_of_order_clas == order else 0

        for vehicle in ["electric_scooter", "motorcycle"]:
            raw_input_clas[f"Type_of_vehicle_{vehicle}"] = 1 if vehicle_type_clas.lower().replace(" ", "_") == vehicle else 0

        for city in ["Urban"]:
            raw_input_clas[f"City_{city}"] = 1 if city_type_clas == city else 0

        input_df_clas = pd.DataFrame([raw_input_clas])
        input_df_clas = input_df_clas.reindex(columns=expected_cols_clas, fill_value=0)

        with st.expander("📋 Input Summary (Classification)"):
            st.dataframe(input_df_clas)

        if "history_clas" not in st.session_state:
            st.session_state.history_clas = []

        if st.button("Predict Delivery Speed", key='predict_clas'):
            try:
                pred_clas = model_clas.predict(input_df_clas)
                prob_clas = model_clas.predict_proba(input_df_clas)
                label_clas = "Slow Delivery" if pred_clas[0] == 1 else "Fast Delivery"
                fast_prob_clas = round(prob_clas[0][0] * 100, 2)  # prob untuk class 0 (Fast)
                slow_prob_clas = round(prob_clas[0][1] * 100, 2)  # prob untuk class 1 (Slow)

                st.warning(f"Prediction Result: **{label_clas}**")

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    st.markdown("#### Fast Delivery Probability")
                    st.markdown(f"<h3 style='color: green; font-weight:bold;'>{fast_prob_clas:.2f}%</h3>", 
                              unsafe_allow_html=True)
                with col2:
                    st.markdown("#### Slow Delivery Probability")
                    st.markdown(f"<h3 style='color:red; font-weight:bold;'>{slow_prob_clas:.2f}%</h3>", 
                              unsafe_allow_html=True)
                with col3:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=slow_prob_clas,
                        title={'text': "Delivery Speed Probability"},
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

                input_df_clas["Fast Delivery Probability"] = fast_prob_clas
                input_df_clas["Slow Delivery Probability"] = slow_prob_clas
                st.session_state.history_clas.append(input_df_clas)

            except Exception as e:
                st.error(f"Prediction failed: {str(e)}")

        st.markdown("#### History Data")
        if st.session_state.history_clas:
            hist_df_clas = pd.concat(st.session_state.history_clas, ignore_index=True)
            st.dataframe(hist_df_clas)
        else:
            st.info("No input history available.")

        if st.button("Reset History", key='reset_clas'):
            st.session_state.history_clas = []
            st.rerun()

if __name__ == "__main__":
    app()