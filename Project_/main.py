import streamlit as st
from streamlit_option_menu import option_menu
from pages import about, contact, dashboard_churn, dashboard_sentiment, prediction_churn, prediction_sentiment

st.set_page_config(page_title="Portofolio", page_icon="📌", layout="centered")

with st.sidebar:
    st.title("Navigation")
    
    menu = option_menu(
        "Main Menu",
        ["About", "Dashboard", "Prediction", "Contact"],
        icons=["house", "bar-chart", "robot", "telephone"],
        menu_icon="list",
        default_index=0,
        styles={
            "nav-link-hover": {"background-color": "#f0f2f6", "color": "#3b82f6", "border-radius": "10px", "transition": "all 0.3s"},
            "nav-link-selected": {"background-color": "#3b82f6", "color": "white"}})

    submenu = None
    if menu == "Dashboard": submenu = st.radio(
            "Select Dashboard", ["Customer Churn", "Customer Satisfaction"], 
            format_func=lambda x: f"📈 {x}" if "Churn" in x else f"😊 {x}")
            
    elif menu == "Prediction": submenu = st.radio(
            "Select Prediction", ["Customer Churn", "Customer Satisfaction"],
            format_func=lambda x: f"📋 {x}" if "Churn" in x else f"💬 {x}")

if menu == "About":
    about.about_me()
elif menu == "Dashboard" and submenu == "Customer Churn":
    dashboard_churn.dashboard_churn()
elif menu == "Dashboard" and submenu == "Customer Satisfaction":
    dashboard_sentiment.dashboard_sentiment()
elif menu == "Prediction" and submenu == "Customer Churn":
    prediction_churn.prediction_churn()
elif menu == "Prediction" and submenu == "Customer Satisfaction":
    prediction_sentiment.prediction_sentiment()
elif menu == "Contact":
    contact.contact_me()

if menu != "Contact":
    st.markdown("---")
    st.write(f"**You are viewing the {menu}{' - ' + submenu if submenu else ''} page!**")
