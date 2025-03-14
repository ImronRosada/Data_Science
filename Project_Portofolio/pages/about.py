import streamlit as st
from PIL import Image

def about_me():
    image = Image.open("file/background.jpg").convert("RGBA")
    st.image(image, width=200)

    st.title("About Me")
    st.write(
        "Hello! I am Imron Rosada, a Data Scientist & Machine Learning Enthusiast with experience in data analysis, predictive modeling, and data visualization." 
        "I have expertise in Python, SQL, and various tools such as Streamlit, Power BI, Tableau, and Web Development technologies."
    )

    st.subheader("Main Skills")
    tab1, tab2, tab3 = st.tabs(["💻 Programming", "📊 Data Science", "🌐 Web Development"])
    with tab1:
        st.markdown("### Programming & Databases")
        st.markdown("✅ **Python** (Pandas, NumPy, Scikit-learn, Streamlit)")
        st.markdown("✅ **SQL** (PostgreSQL, MySQL)")
    with tab2:
        st.markdown("### Data Science & Visualization")
        st.markdown("✅ **Machine Learning** (Supervised & Unsupervised Learning, Model Tuning, Hyperparameter Optimization, Model Deployment)")
        st.markdown("✅ **Data Visualization** (Matplotlib, Seaborn, Plotly, Power BI, Tableau)")
        st.markdown("✅ **Business Intelligence & Dashboard Development**")
    with tab3:
        st.markdown("### Web Development")
        st.markdown("✅ **HTML, CSS, JavaScript** (Frontend Development)")
        st.markdown("✅ **PHP** (Backend Development)")
