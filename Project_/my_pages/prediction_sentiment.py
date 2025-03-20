import streamlit as st
import pandas as pd
import re
import plotly.express as px
import nltk
import os
from nltk.sentiment import SentimentIntensityAnalyzer
# st.write("Current working directory:", os.getcwd())
# st.write("Files in cwd:", os.listdir())
# Clear Streamlit cache (you can clear cache programmatically here if needed)
st.cache_data.clear()
st.cache_resource.clear()

# Download lexicon untuk analisis sentimen
nltk.download("vader_lexicon")

# Inisialisasi model VADER
vader_model = SentimentIntensityAnalyzer()

# Fungsi membersihkan teks
def cleansing_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"http\S+|www\S+", "http", text)
    text = re.sub(r"@\S+", "@user", text)
    return text

# Fungsi prediksi sentimen menggunakan VADER
def predict_vader(text):
    score = vader_model.polarity_scores(text)
    compound = score["compound"]
    return "Positive" if compound >= 0.05 else "Negative" if compound <= -0.05 else "Neutral"

# Menampilkan hasil prediksi dengan ikon emosi
def show_prediction_result(sentiment):
    if sentiment == "Positive":
        st.success(f"**Prediction Result:** {sentiment} 😀")
    elif sentiment == "Neutral":
        st.warning(f"**Prediction Result:** {sentiment} 😐")
    else:
        st.error(f"**Prediction Result:** {sentiment} 😡")

# Fungsi utama untuk prediksi sentimen
def prediction_sentiment():
    st.title("Sentiment Prediction")
    st.info("Model Prediction using **VADER** (lexicon-based)")

    tab1, tab2 = st.tabs(["📊 Default Data", "✍️ Manual Input"])

    # **Pastikan session state history ada**
    if "history" not in st.session_state:
        st.session_state["history"] = []
    
    if "manual_history" not in st.session_state:
        st.session_state["manual_history"] = []

    # Tab pertama: Menggunakan dataset default
    with tab1:
        file_path = "Project_/dataset/ticket_system_review_processed.csv"

        if not os.path.exists(file_path):
            st.error(f"⚠️ Dataset not found: {file_path}")
            return

        try:
            df = pd.read_csv(file_path, parse_dates=["date_of_survey"])
        except Exception as e:
            st.error(f"⚠️ Failed to load dataset. Error: {e}")
            return

        if "overall_text" not in df.columns:
            st.error("⚠️ The dataset must have a column 'overall_text'.")
            return

        # Membersihkan teks
        df["overall_text"] = df["overall_text"].fillna("").astype(str)
        df["clean_text"] = df["overall_text"].apply(cleansing_text)
        df["predicted_sentiment"] = df["clean_text"].apply(predict_vader)

        # Hapus baris dengan teks kosong
        df = df[df["overall_text"].str.strip() != ""]

        # Fungsi untuk UI berdasarkan kategori sentimen
        def sentiment_tab_ui(sentiment_label):
            filtered_df = df[df["predicted_sentiment"] == sentiment_label]

            if filtered_df.empty:
                st.warning(f"No data available with {sentiment_label} sentiment.")
                return

            st.dataframe(filtered_df[["overall_text"]], height=300)

            selected_reviews = st.multiselect(
                f"Select reviews with {sentiment_label} sentiment:",
                filtered_df["overall_text"].unique(),
                help="Choose reviews from the dataset for sentiment analysis.",
            )

            if selected_reviews:
                for review in selected_reviews:
                    sentiment_result = predict_vader(review)
                    # **Cegah duplikasi dalam history**
                    if {"Review": review, "Sentiment": sentiment_result} not in st.session_state["history"]:
                        st.session_state["history"].append({"Review": review, "Sentiment": sentiment_result})

            if st.button(f"🔄 Reset {sentiment_label} Predictions"):
                if selected_reviews:
                    st.warning("⚠️ Reset is disabled while reviews are selected. Please deselect all reviews first.")
                else:
                    st.session_state["history"] = []
                    st.rerun()

        # Menampilkan data berdasarkan sentimen
        tab_pos, tab_neu, tab_neg = st.tabs(["😀 Positive", "😐 Neutral", "😡 Negative"])

        with tab_pos:
            sentiment_tab_ui("Positive")

        with tab_neu:
            sentiment_tab_ui("Neutral")

        with tab_neg:
            sentiment_tab_ui("Negative")

        # **Menampilkan history hanya jika ada data**
        if st.session_state["history"]:
            st.markdown("#### Prediction Results")

            history_df = pd.DataFrame(st.session_state["history"]) if st.session_state["history"] else pd.DataFrame(columns=["Review", "Sentiment"])

            if not history_df.empty:
                sentiment_counts = history_df["Sentiment"].value_counts().reset_index()
                sentiment_counts.columns = ["Sentiment", "Count"]
                fig_pie = px.pie(sentiment_counts, names="Sentiment", values="Count", title="Sentiment Distribution")
                st.plotly_chart(fig_pie)

                st.markdown("#### Prediction History")
                st.dataframe(history_df, use_container_width=True)

                if st.button("🔄 Reset History"):
                    st.session_state["history"] = []
                    st.rerun()

    # Tab kedua: Input manual
    with tab2:
        review_text = st.text_area(
            "Enter your review here:",
            "",
            placeholder="Only English text is supported.",
            help="Type a review for sentiment prediction.",
        )

        if st.button("🔮 Predict"):
            if review_text.strip():
                clean_text = cleansing_text(review_text)
                sentiment_result = predict_vader(clean_text)
                show_prediction_result(sentiment_result)

                # **Cegah duplikasi dalam manual history**
                if {"Review": review_text, "Sentiment": sentiment_result} not in st.session_state["manual_history"]:
                    st.session_state["manual_history"].append({"Review": review_text, "Sentiment": sentiment_result})
            else:
                st.warning("⚠️ Please enter a review before predicting.")

        # **Tampilkan history manual hanya jika ada data**
        if st.session_state["manual_history"]:
            st.markdown("#### Manual Input History")
            manual_df = pd.DataFrame(st.session_state["manual_history"])

            st.dataframe(manual_df, use_container_width=True)

            if st.button("🔄 Reset History"):
                st.session_state["manual_history"] = []
                st.rerun()

# Jalankan fungsi utama
if __name__ == "__main__":
    prediction_sentiment()