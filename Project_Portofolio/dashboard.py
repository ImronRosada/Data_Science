
import streamlit as st
import pandas as pd
import plotly.express as px

# Clear Streamlit cache (you can clear cache programmatically here if needed)
st.cache_data.clear()
st.cache_resource.clear() 

def dashboard():
    st.title("Dashboard")

    df = pd.read_csv("df_churn_cleaned.csv")
    df["Exited"] = df["Exited"].replace({0: "No Churn", 1: "Churn"})

    st.sidebar.header("🔍 Filter Options")
    gender_filter = st.sidebar.selectbox("Select Gender:", options=["All"] + list(df["Gender"].unique()))
    geo_filter = st.sidebar.selectbox("Select Geography:", options=["All"] + list(df["Geography"].unique()))

    filtered_df = df.copy()
    if gender_filter != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]
    if geo_filter != "All":
        filtered_df = filtered_df[filtered_df["Geography"] == geo_filter]

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "👥 Customer Characteristics", "📅 Age & Tenure", "💰 Financial Factors", "🏦 Finance & Activity"])
    
    with tab1:
        st.subheader("Churn Status Distribution")
        data = filtered_df["Exited"].value_counts().reset_index()
        data.columns = ["Churn Status", "Count"]
        fig = px.bar(data, x="Churn Status", y="Count", color="Churn Status",
                    color_discrete_sequence=px.colors.qualitative.Set2, text="Count", text_auto=True)
        fig.update_layout(xaxis_title="",  yaxis_title="", legend_title_text="")    
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Churn and Customer Characteristics")
        data_gender_geography = pd.crosstab([filtered_df["Gender"], filtered_df["Geography"]], filtered_df["Exited"]).T
        data_long = data_gender_geography.T.stack().reset_index()
        data_long.columns = ['Gender', 'Geography', 'Exited', 'Count']
        fig = px.bar(data_long, x='Gender', y='Count', color='Geography', facet_col='Exited',
                     barmode='group', text_auto=True)
        fig.update_layout(yaxis_title="", legend_title_text="")
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Churn by Age and Tenure")
        
        # a. Age Group and Activity Status
        st.markdown("Age Group and Activity Status")
        data_age_active = pd.crosstab(
            index=filtered_df['Exited'],
            columns=[filtered_df['AgeGroup'], filtered_df['Age_ActiveStatus']]
        )
        data_long = data_age_active.T.stack().reset_index()
        data_long.columns = ['AgeGroup', 'Age_ActiveStatus', 'Exited', 'Count']
        fig = px.pie(data_long, names='Age_ActiveStatus', values='Count', facet_col='Exited')
        st.plotly_chart(fig, use_container_width=True)
        
        # b. Tenure
        st.markdown("Tenure")
        data_tenure_group = filtered_df.groupby(["TenureGroup", "Exited"], observed=True).size().unstack().T
        data_long = data_tenure_group.T.stack().reset_index()
        data_long.columns = ['TenureGroup', 'Exited', 'Count']
        fig = px.scatter(data_long, x='TenureGroup', y='Exited', size='Count', color='Exited')
        fig.update_layout(legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Churn and Financial Factors")
        
        # a. Balance Category
        st.markdown("Balance Category")        
        data_balance = pd.crosstab(filtered_df["BalanceCategory"], filtered_df["Exited"]).T
        data_long = data_balance.T.stack().reset_index()
        data_long.columns = ['BalanceCategory', 'Exited', 'Count']
        fig = px.pie(data_long, names='BalanceCategory', values='Count', facet_col='Exited', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

        # b. Credit Score Group
        st.markdown("Credit Score Group") 
        data_credit = filtered_df.groupby(["CreditScoreGroup", "Exited"], observed=False).size().unstack().T
        data_long = data_credit.T.stack().reset_index()
        data_long.columns = ['CreditScoreGroup', 'Exited', 'Count']
        fig = px.scatter(data_long, x='CreditScoreGroup', y='Count', color='Exited', size='Count')
        fig.update_layout(yaxis_title="", legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.subheader("Churn and Financial Activity")
        
        # a. Credit Score and Bank Products Used
        st.markdown("Credit Score and Bank Products Used")
        skor_jumlah_produk = pd.crosstab(
            index=[filtered_df["CreditScore"], filtered_df["NumOfProducts"]],
            columns=filtered_df["Exited"]
        )
        data_long = skor_jumlah_produk.stack().reset_index()
        data_long.columns = ['CreditScore', 'NumOfProducts', 'Exited', 'Count']
        fig = px.histogram(data_long, x='CreditScore', y='Count', color='Exited', facet_col='NumOfProducts', nbins=20)
        fig.update_layout(yaxis_title="", legend_title_text="")        
        st.plotly_chart(fig, use_container_width=True)
        
        # b. Credit Card, Active Membership, and Salary Category
        st.markdown("Credit Card, Active Membership, and Salary Category")
        data_crcard_active_salary = pd.crosstab([filtered_df["HasCrCard"], filtered_df["IsActiveMember"], filtered_df["EstimatedSalaryCategory"]], filtered_df["Exited"]).T
        data_crcard_active_salary.columns = data_crcard_active_salary.columns.set_levels(["No", "Yes"], level=0)
        data_crcard_active_salary.columns = data_crcard_active_salary.columns.set_levels(["Inactive", "Active"], level=1)
        data_long = data_crcard_active_salary.stack(level=[0, 1, 2], future_stack=True).reset_index()
        data_long.columns = ['Exited', 'HasCrCard', 'IsActiveMember', 'EstimatedSalaryCategory', 'Count']
        fig = px.bar(data_long, x='EstimatedSalaryCategory', y='Count', color='Exited', facet_row='HasCrCard', facet_col='IsActiveMember', barmode='group', text_auto=True)
        fig.update_layout(yaxis_title="", legend_title_text="")
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', '')))
        fig.update_yaxes(title_text='', range=[0, data_long["Count"].max() + 100])
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig)

    st.subheader("📄 Data Displayed")
    st.dataframe(filtered_df)
