import streamlit as st

def app():
    # Inisialisasi tombol close
    if "show_about" not in st.session_state:
        st.session_state.show_about = True

    if st.session_state.show_about:
        st.markdown("<h2 style='text-align: center; color: #3b82f6;'>About Application</h2>", unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <h4>Project – Zomato Delivery Time App</h4>
            <p><strong>Project Title: Delivery Time Operation Analysis and Classification</strong></p>
            <p>
                This application was developed to analyze operational performance in food delivery. 
                The goal is to estimate delivery time accurately and classify deliveries into "Fast" or "Slow" categories using machine learning models.
            </p>
            <p><strong>Main Components:</strong></p>
            <ul>
                <li><strong>Dashboard:</strong> Visualizes delivery duration patterns, speed categories, and overall operational performance.</li>
                <li><strong>Prediction:</strong> Estimates delivery time using regression and classifies delivery speed using classification models.</li>
                <li><strong>Recommendations:</strong> Provides actionable insights based on model performance to improve delivery operations.</li>
            </ul>
            <p>This project integrates statistical analysis, machine learning, and interactive visualization using Python and Streamlit.</p>
            """, unsafe_allow_html=True)
        st.markdown("")  # spacing
        if st.button("Close About"):
            st.session_state.selected_page = "Dashboard"
            st.session_state.show_about = False
            
if __name__ == "__main__":
    app()