import streamlit as st

def contact_me():

    st.subheader("Let's Get in Touch! 🌟")
    contact_tab1, contact_tab2 = st.tabs(["📩 Email & LinkedIn", "📱 WhatsApp & GitHub"])
    
    with contact_tab1:
        st.write("Feel free to reach out to me via email or LinkedIn!")
        st.write("📧 **Email    :** [Sent Me email to imronr91@gmail.com](mailto:imronr91@gmail.com)")
        st.write("🔗 **LinkedIn :** [Connect with me on LinkedIn](https://www.linkedin.com/in/imron-rosada/)")
    
    with contact_tab2:
        st.write("For a more direct conversation, you can contact me via WhatsApp or explore my work on GitHub!")
        st.write("📱 **WhatsApp :** [Chat with me on WhatsApp](https://wa.me/6281220631122)")
        st.write("📂 **GitHub   :** [Explore my projects on GitHub](https://github.com/ImronRosada/)")
