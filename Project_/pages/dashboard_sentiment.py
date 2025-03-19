import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
# import os
# st.write("Current working directory:", os.getcwd())
# st.write("Files in cwd:", os.listdir())
# Clear Streamlit cache (you can clear cache programmatically here if needed)
st.cache_data.clear()
st.cache_resource.clear() 

def dashboard_sentiment():
    st.title("Customer Satisfaction Dashboard")
    
    # Load dataset
    df = pd.read_csv("dataset/ticket_system_review.csv", parse_dates=["date_of_survey"])
    
    # Create 'fill_survey' column
    df['fill_survey'] = np.where(df['overall_rating'].isnull(), 'Not Responded', 'Responded')
    
    # Add customer satisfaction column
    df['customer_satisfaction'] = np.where(df['overall_rating'] >= 4, 'Satisfied', 'Not Satisfied')
    
    # Sidebar filters
    st.sidebar.header("🔍 Filter Options")
    ticket_filter = st.sidebar.selectbox("Select Ticket System:", options=["All"] + list(df["ticket_system"].dropna().unique()))
    date_range = st.sidebar.date_input("Select Date Range:", 
                                       value=[df["date_of_survey"].min(), df["date_of_survey"].max()], 
                                       min_value=df["date_of_survey"].min(), 
                                       max_value=df["date_of_survey"].max())

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)

    # Filter Data
    filtered_df = df.copy()
    if ticket_filter and ticket_filter != "All":
        filtered_df = filtered_df[filtered_df["ticket_system"] == ticket_filter]
    filtered_df = filtered_df[(filtered_df["date_of_survey"] >= start_date) & (filtered_df["date_of_survey"] <= end_date)]
    responded_customer = filtered_df[filtered_df['fill_survey'] == 'Responded'].copy()
    
    # Recalculate Metrics
    max_rating_5, max_rating_10 = 5, 10
    csat_score_overall = responded_customer['overall_rating'].sum() / (responded_customer.shape[0] * max_rating_5) if responded_customer.shape[0] > 0 else 0
    responded_customer['is_satisfied'] = np.where(responded_customer['overall_rating'] >= 4, 1, 0)
    positive_csat = responded_customer['is_satisfied'].mean() * 100 if responded_customer.shape[0] > 0 else 0
    ces_ease_of_use = responded_customer['ease_of_use'].sum() / (responded_customer.shape[0] * max_rating_5) if responded_customer.shape[0] > 0 else 0
    ces_likelihood_to_recommend = responded_customer['likelihood_to_recommend'].sum() / (responded_customer.shape[0] * max_rating_10) if responded_customer.shape[0] > 0 else 0
    
    responded_customer['nps_category'] = np.select([
        responded_customer['likelihood_to_recommend'] >= 9,
        (responded_customer['likelihood_to_recommend'] >= 7) & (responded_customer['likelihood_to_recommend'] <= 8),
        responded_customer['likelihood_to_recommend'] < 7
    ], ['Promoter', 'Passive', 'Detractor'], default="Unknown")
    nps_agg = responded_customer['nps_category'].value_counts().reset_index()
    nps_agg.columns = ['nps_category', 'count']
    nps_score = (nps_agg[nps_agg['nps_category'] == 'Promoter']['count'].sum() -
                 nps_agg[nps_agg['nps_category'] == 'Detractor']['count'].sum()) / responded_customer.shape[0] * 100 if responded_customer.shape[0] > 0 else 0

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔄 Overview", "📊 NPS Metrics", "📊 CSAT & CES", "📉 Score Over Time", "📝 Survey by Ticket", "📆 Survey by Date"])
    
    with tab1:
        st.subheader("Survey Response")
        response_counts = filtered_df["fill_survey"].value_counts()
        response_data = pd.DataFrame({"Status": response_counts.index, "Count": response_counts.values})
        st.plotly_chart(px.pie(response_data, names="Status", values="Count", hole=0.4), use_container_width=True)
    with tab2:
        st.subheader("NPS Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("NPS Score")
            st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=nps_score, gauge={"axis": {"range": [-100, 100]}})), use_container_width=True)
        with col2:
            st.subheader("NPS Category")
            fig = px.bar(nps_agg, x="nps_category", y="count", text_auto=True, color="nps_category")
            fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title_text=None)
            st.plotly_chart(fig, use_container_width=True)    
    with tab3:
        st.subheader("CSAT & CES")
        col3, col4, col5, col6 = st.columns(4)
        with col3: st.metric("Overall CSAT", f"{csat_score_overall * 100:.1f}%")
        with col4: st.metric("Positive CSAT", f"{positive_csat:.1f}%")
        with col5: st.metric("Ease of Use CES", f"{ces_ease_of_use * 100:.1f}%")
        with col6: st.metric("Likelihood CES", f"{ces_likelihood_to_recommend * 100:.1f}%")
    
    with tab4:
        st.subheader("Score Over Time")
        
        # Menghitung skor rata-rata setiap metrik berdasarkan tanggal
        score_data = filtered_df.groupby("date_of_survey")[["likelihood_to_recommend", "overall_rating", "ease_of_use"]].mean().reset_index()
        score_data = score_data.melt(id_vars=["date_of_survey"], var_name="Metric", value_name="Score")

        # Menghitung NPS Score per tanggal
        nps_score_data = filtered_df.groupby("date_of_survey").apply(
            lambda x: ((x["likelihood_to_recommend"] >= 9).sum() - (x["likelihood_to_recommend"] <= 6).sum()) / len(x) * 100
        ).reset_index()
        nps_score_data.columns = ["date_of_survey", "Score"]
        nps_score_data["Metric"] = "NPS Score"
        
        # Gabungkan dengan data lainnya
        score_data = pd.concat([score_data, nps_score_data])

        # Plot
        fig = px.line(score_data, x="date_of_survey", y="Score", color="Metric", markers=True)
        fig.update_layout(xaxis_title=None, yaxis_title="Score", legend_title_text=None)
        st.plotly_chart(fig, use_container_width=True)


    with tab5:
        st.subheader("Survey by Ticket System")
        survey_by_ticket = filtered_df["ticket_system"].value_counts().reset_index()
        survey_by_ticket.columns = ["Ticket System", "Survey Count"]
        fig = px.bar(survey_by_ticket, y="Ticket System", x="Survey Count", text_auto=True, color="Ticket System", orientation='h')
        fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title_text=None)
        st.plotly_chart(fig, use_container_width=True)   
    with tab6:
        st.subheader("Survey by Date")
        survey_by_date = filtered_df["date_of_survey"].value_counts().reset_index()
        survey_by_date.columns = ["Date", "Survey Count"]
        fig = px.bar(survey_by_date, x="Date", y="Survey Count", text_auto=True)
        fig.update_layout(xaxis_title=None, yaxis_title=None, legend_title_text=None)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📄 Data Displayed")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    dashboard_sentiment()
