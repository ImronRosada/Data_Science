import streamlit as st
from streamlit_option_menu import option_menu

# Clear Streamlit cache (you can clear cache programmatically here if needed)
st.cache_data.clear()
st.cache_resource.clear() 

# Set page config
st.set_page_config(page_title="Portofolio", page_icon="📌", layout="centered")

# Sidebar menu using option_menu
with st.sidebar:
    st.title("Navigation")
    menu = option_menu(
        "Main Menu", ["About Me", "Dashboard", "Prediction", "Contact Me"],
        icons=["house", "bar-chart", "robot", "telephone"],
        menu_icon="list",
        default_index=0,
        styles={
            "nav-link-hover": {"background-color": "#f0f2f6", "color": "#3b82f6", "border-radius": "10px", "transition": "all 0.3s"},
            "nav-link-selected": {"background-color": "#3b82f6", "color": "white"}
        }
    )

# Display content based on sidebar menu selection
if menu == "About Me":
    import about
    about.about_me()
elif menu == "Dashboard":
    import dashboard
    dashboard.dashboard()
elif menu == "Prediction":
    import prediction
    prediction.prediction()
elif menu == "Contact Me":
    import contact
    contact.contact_me()

# Add some interactivity by displaying a welcome message or a footer message
if menu != "Contact Me":  # Avoid cluttering the Contact page
    st.markdown("---")
    st.write(f"**You are viewing the {menu} page!**")
