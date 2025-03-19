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
# Clear Streamlit cache
st.cache_data.clear()
st.cache_resource.clear()

nltk.download('vader_lexicon')

vader_model = SentimentIntensityAnalyzer()

def cleansing_text(text):
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"http\S+|www\S+", "http", text)
    text = re.sub(r"@\S+", "@user", text)
    return text

def predict_vader(text):
    score = vader_model.polarity_scores(text)
    compound = score["compound"]
    return "Positive" if compound >= 0.05 else "Negative" if compound <= -0.05 else "Neutral"

def show_prediction_result(sentiment):
    if sentiment == "Positive":
        st.success(f"**Prediction Result:** {sentiment} 😀")
    elif sentiment == "Neutral":
        st.warning(f"**Prediction Result:** {sentiment} 😐")
    else:
        st.error(f"**Prediction Result:** {sentiment} 😡")

def prediction_sentiment():
    st.title("Sentiment Prediction")
    st.info("Model Prediction using **VADER** (lexicon-based)")

    tab1, tab2 = st.tabs(["📊 Default Data", "✍️ Manual Input"])

    with tab1:
        file_path = "dataset/ticket_system_review_processed.csv"

        if not os.path.exists(file_path):
            st.error(f"Dataset not found: {file_path}")
            return

        try:
            df = pd.read_csv(file_path, parse_dates=["date_of_survey"])
        except Exception as e:
            st.error(f"⚠️ Failed to load dataset. Error: {e}")
            return

        st.info("Please fill in the data below according to the instructions.")
        if "overall_text" not in df.columns:
            st.error("⚠️ The dataset must have a column 'overall_text'.")
            return

        df["overall_text"] = df["overall_text"].fillna("").astype(str)
        df["clean_text"] = df["overall_text"].apply(cleansing_text)
        df["predicted_sentiment"] = df["clean_text"].apply(predict_vader)

        df = df[df["overall_text"].str.strip() != ""]

        tab_pos, tab_neu, tab_neg = st.tabs(["😀 Positive", "😐 Neutral", "😡 Negative"])

        if "history" not in st.session_state:
            st.session_state["history"] = []

        def sentiment_tab_ui(sentiment_label):
            filtered_df = df[df["predicted_sentiment"] == sentiment_label]
            
            if filtered_df.empty:
                st.warning(f"No data available with {sentiment_label} sentiment.")
                return
            
            st.dataframe(filtered_df[["overall_text"]], height=300)
            
            selected_reviews = st.multiselect(
                f"Select reviews with {sentiment_label} sentiment:",
                filtered_df["overall_text"].unique(),
                help="Choose reviews from the dataset for sentiment analysis."
            )
            
            if selected_reviews:
                for review in selected_reviews:
                    sentiment_result = predict_vader(review)
                    st.session_state["history"].append({"Review": review, "Sentiment": sentiment_result})

        with tab_pos:
            sentiment_tab_ui("Positive")

        with tab_neu:
            sentiment_tab_ui("Neutral")

        with tab_neg:
            sentiment_tab_ui("Negative")

        if st.session_state["history"]:
            st.markdown("#### Prediction Results")
            history_df = pd.DataFrame(st.session_state["history"])

            sentiment_counts = history_df["Sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            fig_pie = px.pie(sentiment_counts, names="Sentiment", values="Count", title="Sentiment Distribution")
            st.plotly_chart(fig_pie)

            st.markdown("#### Prediction History")
            st.dataframe(history_df, use_container_width=True)

            if st.button("🔄 Reset Predictions"):
                st.session_state["history"] = []
                st.rerun()

    with tab2:
        review_text = st.text_area("Enter your review here:", "", placeholder="Only text English is supported.", help="Type a review for sentiment prediction.")

        if "manual_history" not in st.session_state:
            st.session_state["manual_history"] = []

        if st.button("🔮 Predict"):
            if review_text.strip():
                clean_text = cleansing_text(review_text)
                sentiment_result = predict_vader(clean_text)
                show_prediction_result(sentiment_result)
                st.session_state["manual_history"].append({"Review": review_text, "Sentiment": sentiment_result})
            else:
                st.warning("⚠️ Please enter a review before predicting.")

        if st.session_state["manual_history"]:
            st.markdown("#### Manual Input History")
            manual_df = pd.DataFrame(st.session_state["manual_history"])
            st.dataframe(manual_df, use_container_width=True)

            if st.button("🔄 Reset History"):
                st.session_state["manual_history"] = []
                st.rerun()

if __name__ == "__main__":
    prediction_sentiment()
