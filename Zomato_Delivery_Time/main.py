import streamlit as st
from streamlit_option_menu import option_menu

# Import pages from my_pages
from my_pages import (dashboard, prediction, about, insights) 

# Page configuration
st.set_page_config(page_title="Zomato Delivery Time Operation", page_icon="🛵️", layout="wide")

# Inisialisasi session_state jika belum ada
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"

# Sidebar navigation
with st.sidebar:
    st.image("Zomato_Delivery_Time/img/zomato2.jpg", width=400)
    st.title("Zomato Delivery Time App")
    st.caption("*Food Delivery Operation Analysis and Prediction*")

    # Feature menu
    st.markdown("## Feature Menu")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Prediction", "Insights"],  # Tambahkan "Insights"
        icons=["bar-chart-line", "graph-up-arrow", "lightbulb"],  # Tambahkan ikon untuk Insights
        default_index=0,
        styles={
            "nav-link-hover": {"background-color": "#f0f2f6", "color": "#3b82f6", "border-radius": "10px", "transition": "all 0.3s"},
            "nav-link-selected": {"background-color": "#3b82f6", "color": "white"}
        }
    )
    st.session_state.selected_page = selected

    if st.button("ℹ️ About Application"):
        st.session_state.selected_page = "About Application"

    st.markdown("---")

# Routing based on selected menu
st.empty()  # spacing

if st.session_state.selected_page == "Dashboard":
    dashboard.app()
elif st.session_state.selected_page == "Prediction":
    prediction.app()
elif st.session_state.selected_page == "Insights": 
    insights.app()
elif st.session_state.selected_page == "About Application":
    about.app()

# Footer
st.markdown("---")
st.write(f"**You are viewing the `{st.session_state.selected_page}` page!**")