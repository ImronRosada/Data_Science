import streamlit as st

def app():
    # Inisialisasi tombol close
    if "show_about" not in st.session_state:
        st.session_state.show_about = True

    if st.session_state.show_about:
        st.markdown("<h2 style='text-align: center; color: #3b82f6;'>About Application</h2>", unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div style="background-color: #f0f2f6; padding: 25px; border-radius: 15px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); font-size: 16px;">
                <h4 style="color: #3b82f6;">Final Project – Data Science Bootcamp</h4>
                <p><strong>Project Title:</strong> Credit Card Customer Analysis and Churn Prediction</p>
                <p>
                    This application was developed as part of a final project for the Data Science Bootcamp program. 
                    The objective is to analyze customer behavior related to credit card usage and develop a predictive model to identify potential customer churn.
                </p>
                <p><strong>Key Features:</strong></p>
                <ul>
                    <li><strong>Dashboard:</strong> Provides an overview of customer demographics, behavior, and churn trends.</li>
                    <li><strong>Prediction:</strong> Allows users to input customer data and receive churn probability predictions.</li>
                    <li><strong>Insights:</strong> Offers actionable insights to support strategic decision-making in customer retention.</li>
                </ul>
                <p>This project applies statistical analysis, data visualization, and machine learning methodologies using Python and Streamlit.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("")  # spacing
        if st.button("Close About"):
            st.session_state.selected_page = "Dashboard"
            st.session_state.show_about = False
            
if __name__ == "__main__":
    app()