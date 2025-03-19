import streamlit as st

# Clear Streamlit cache (you can clear cache programmatically here if needed)
st.cache_data.clear()
st.cache_resource.clear() 

def about_me():
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
        
if __name__ == "__main__":
    about_me()