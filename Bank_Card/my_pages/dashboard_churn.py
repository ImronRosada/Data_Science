import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📊 Customer Dashboard - Bank Credit Card")
    
    # Load dataset
    df_churn = pd.read_csv("Bank_Card/dataset/df_churn.csv")

    # Preprocessing ringan jika diperlukan
    df_churn["Gender"] = df_churn["Gender"].astype("category").cat.rename_categories({"F": "Female", "M": "Male"})

    # Filter
    st.sidebar.header("🔍 Filter Options")
    gender_filter = st.sidebar.multiselect("Select Gender:", df_churn["Gender"].unique(), default=df_churn["Gender"].unique(),  help="Filter data based on customer's gender.")
    churn_filter = st.sidebar.multiselect("Churn Status:", df_churn["Attrition_Flag"].unique(), default=df_churn["Attrition_Flag"].unique(), help="Choose whether to display churned or existing customers.")

    age_filter = st.sidebar.slider("Customer Age Range:", int(df_churn["Customer_Age"].min()), int(df_churn["Customer_Age"].max()), (int(df_churn["Customer_Age"].min()), int(df_churn["Customer_Age"].max())), help="Select a range of customer ages to include in the analysis.")
    trans_ct_filter = st.sidebar.slider("Total Transactions Range:", int(df_churn["Total_Trans_Ct"].min()), int(df_churn["Total_Trans_Ct"].max()), (int(df_churn["Total_Trans_Ct"].min()), int(df_churn["Total_Trans_Ct"].max())), help="Filter by the number of transactions made by customers.")
    trans_amt_filter = st.sidebar.slider("Total Transaction Amount Range:", float(df_churn["Total_Trans_Amt"].min()), float(df_churn["Total_Trans_Amt"].max()), (float(df_churn["Total_Trans_Amt"].min()), float(df_churn["Total_Trans_Amt"].max())), help="Select a range of total transaction amounts for filtering customers.")

    # Apply Filter ke DataFrame
    df_churn = df_churn[
    (df_churn["Gender"].isin(gender_filter)) &
    (df_churn["Customer_Age"].between(age_filter[0], age_filter[1])) &
    (df_churn["Total_Trans_Ct"].between(trans_ct_filter[0], trans_ct_filter[1])) &
    (df_churn["Total_Trans_Amt"].between(trans_amt_filter[0], trans_amt_filter[1])) &
    (df_churn["Attrition_Flag"].isin(churn_filter))
    ]

    # Tab layout
    tabs = st.tabs([
        "📊 Overview",
        "👥 Demographics & Social",
        "🧭 Behavior & Account Activity",
        "💰 Financial & Credit Limit",
        "💳 Transactions & Usage",
        "🧾 Products & Card Categories"
    ])

    # === TAB 0: Overview ===
    with tabs[0]:
        st.markdown("##### Churn Status Distribution")
        churn_count = df_churn['Attrition_Flag'].value_counts().reset_index()
        churn_count.columns = ['Attrition_Flag', 'Count']

        fig = px.bar(churn_count, x='Count', y='Attrition_Flag',
                    orientation='h', color='Attrition_Flag', text_auto=True, labels={'Count': '', 'Attrition_Flag': ''},
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(title="", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

    # === TAB 1: Demografi & Sosial ===
    with tabs[1]:
        st.markdown("##### a. Gender")
        data_gender = pd.crosstab(df_churn["Gender"], df_churn["Attrition_Flag"]).T
        data_gender_long = data_gender.T.reset_index().melt(id_vars="Gender", var_name="Attrition_Flag", value_name="Count" ) 
        fig = px.pie( data_gender_long,  names="Gender",   values="Count",  facet_col="Attrition_Flag",  title="Gender Distribution by Churn", color_discrete_sequence=px.colors.qualitative.Antique, labels={"Gender": "", "Count": "", "Attrition_Flag": ""} ) 
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", "")))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### b. Age")
        fig = px.histogram(
            df_churn, x="Customer_Age", color="Attrition_Flag", nbins=60,
            barmode="stack", title="Customer Age Distribution", labels={"Customer_Age": "", "Attrition_Flag": ""},
            color_discrete_sequence=px.colors.qualitative.Pastel, text_auto=True)
        fig.update_layout(xaxis=dict(tickmode="linear"), template="plotly_white")
        fig.update_yaxes(showticklabels=False, title_text="")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### c. Education and Income")
        data_edu_income = pd.crosstab([df_churn["Education_Level"], df_churn["Income_Category"]], df_churn["Attrition_Flag"]).T
        data_long = data_edu_income.T.reset_index().melt(id_vars=["Education_Level", "Income_Category"], var_name="Attrition_Flag", value_name="Count")
        fig = px.scatter(data_long, x="Education_Level", y="Income_Category", size="Count", color="Attrition_Flag", facet_col="Attrition_Flag", title="Churn Distribution by Education and Income",
                        labels={"Count": "", "Education_Level": "", "Income_Category": "", "Attrition_Flag": ""}, color_discrete_map={"Attrited Customer": "red", "Existing Customer": "blue"}, size_max=40)
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", "")))
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### d. Marital Status and Dependents")
        data_marital = pd.crosstab([df_churn["Marital_Status"], df_churn["Dependent_count"]], df_churn["Attrition_Flag"]).stack().reset_index()
        data_marital.columns = ["Marital Status", "Dependent Count", "Churn Status", "Count"]
        fig = px.bar(data_marital, y="Marital Status", x="Count", color="Churn Status", facet_col="Dependent Count", text_auto=True, title="Marital Status & Dependent Count by Churn",
                    labels={"Count": "Count", "Marital Status": "", "Churn Status": ""}, barmode="stack", color_discrete_sequence=px.colors.qualitative.Set1)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_xaxes(title_text="")
        st.plotly_chart(fig, use_container_width=True)

    # === TAB 2: Perilaku & Aktivitas Akun ===
    with tabs[2]:
        st.markdown("##### a. Number of Contacts")
        data_contacts = pd.crosstab(df_churn["Contacts_Count_12_mon"], df_churn["Attrition_Flag"]).stack().reset_index()
        data_contacts.columns = ["Contacts Count (12M)", "Churn Status", "Count"]
        # Perbaikan: color diganti dari "Attrition_Flag" menjadi "Churn Status"
        fig = px.area(data_contacts, x="Contacts Count (12M)", y="Count", color="Churn Status", markers=True, line_shape="spline", title="Account Activity by Contact Count (Last 12 Months)",
                    labels={"Contacts Count (12M)": "", "Count": "", "Churn Status": ""}, color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(xaxis=dict(tickangle=0), template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### b. Customer Tenure")
        data_months = pd.crosstab(df_churn["Months_on_book"], df_churn["Attrition_Flag"]).T
        data_months_long = data_months.T.reset_index().melt(id_vars="Months_on_book", var_name="Attrition_Flag", value_name="Count")
        fig = px.line(data_months_long, x="Months_on_book", y="Count", color="Attrition_Flag", markers=True, title="Trend of Customer Attrition by Months on Book",
                    labels={"Months_on_book": "", "Count": "", "Attrition_Flag": ""}, color_discrete_map={"Existing Customer": "blue", "Attrited Customer": "red"})
        fig.update_layout(xaxis=dict(tickangle=0), template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### c. Total Financial Products or Services")
        data_rel = pd.crosstab(df_churn["Total_Relationship_Count"], df_churn["Attrition_Flag"]).T
        data_rel_long = data_rel.T.reset_index().melt(id_vars="Total_Relationship_Count", var_name="Attrition_Flag", value_name="Count")
        fig = px.line(data_rel_long, x="Total_Relationship_Count", y="Count", color="Attrition_Flag", markers=True, title="Trend of Customer Attrition by Total Relationship Count",
                    labels={"Total_Relationship_Count": "", "Count": "", "Attrition_Flag": ""}, color_discrete_map={"Existing Customer": "blue", "Attrited Customer": "red"})
        fig.update_layout(xaxis=dict(tickangle=0), template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### d. Number of Inactive Months")
        data_inactive = pd.crosstab(df_churn["Months_Inactive_12_mon"], df_churn["Attrition_Flag"]).stack().reset_index()
        data_inactive.columns = ["Months_Inactive_12_mon", "Churn Status", "Count"]
        # Perbaikan: color diganti dari "Attrition_Flag" menjadi "Churn Status"
        fig = px.bar(data_inactive, x="Months_Inactive_12_mon", y="Count", color="Churn Status", barmode="group", title="Customer Attrition by Months of Inactivity", labels={"Months_Inactive_12_mon": "", "Count": "", "Churn Status": ""}, text_auto=True, color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_layout(xaxis=dict(tickmode="linear"), template="plotly_white")
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        st.markdown("##### a. Credit Card Transaction Limit")
        data_credit_cat = pd.crosstab(df_churn["Credit_Limit_Category"], df_churn["Attrition_Flag"]).T
        data_credit_cat_long = data_credit_cat.T.reset_index().melt(id_vars="Credit_Limit_Category", var_name="Attrition_Flag", value_name="Count")
        fig = px.pie(data_credit_cat_long, names="Credit_Limit_Category", values="Count", facet_col="Attrition_Flag", hole=0.4, title="Churn Distribution by Credit Limit Category", labels={"Credit_Limit_Category": "", "Count": "", "Attrition_Flag": ""})
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', '')))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### b. Total Credit Balance")
        category_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
        df_churn['Total_Revolving_Bal_Category'] = pd.Categorical(df_churn['Total_Revolving_Bal_Category'], categories=category_order, ordered=True)
        data_revolving = pd.crosstab(df_churn["Total_Revolving_Bal_Category"], df_churn["Attrition_Flag"]).T
        data_revolving_long = data_revolving.T.reset_index().melt(id_vars="Total_Revolving_Bal_Category", var_name="Attrition_Flag", value_name="Count")
        fig = px.bar(data_revolving_long, x="Total_Revolving_Bal_Category", y="Count", color="Attrition_Flag", barmode="group", title="Churn Distribution by Total Revolving Balance Category",
                    labels={"Total_Revolving_Bal_Category": "", "Count": "", "Attrition_Flag": ""}, text_auto=True, color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(template="plotly_white")
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### c. Average Funds and Credit Limit")
        utilization_order = ['Low Utilization', 'Medium Utilization', 'High Utilization']
        df_churn['Avg_Utilization_Category'] = pd.Categorical(df_churn['Avg_Utilization_Category'], categories=utilization_order, ordered=True)
        avg_open_to_buy_utilization = pd.crosstab([df_churn["Avg_Open_To_Buy_Category"], df_churn["Avg_Utilization_Category"]], df_churn["Attrition_Flag"]).T
        avg_open_to_buy_utilization_long = avg_open_to_buy_utilization.T.reset_index().melt(id_vars=["Avg_Open_To_Buy_Category", "Avg_Utilization_Category"], var_name="Attrition_Flag", value_name="Count")
        fig = px.bar(avg_open_to_buy_utilization_long, x="Count", y="Avg_Open_To_Buy_Category", color="Attrition_Flag", orientation="h", title="Churn by Avg Open To Buy & Utilization Categories", labels={"Count": "", "Avg_Open_To_Buy_Category": "", "Attrition_Flag": "", "Avg_Utilization_Category": ""}, barmode="group", facet_col="Avg_Utilization_Category", text_auto=True, custom_data=["Count"])
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace("=", "")))
        fig.update_traces(hovertemplate="Count: %{customdata[0]}")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[4]:
        st.markdown("##### a. Change in Total Spend and Number of Transactions")
        Total_Amt_Chng = pd.crosstab(index=[df_churn["Total_Amt_Chng_Q4_Q1_Category"], df_churn["Total_Ct_Chng_Q4_Q1_Category"]], columns=df_churn["Attrition_Flag"]).reset_index()
        Total_Amt_Chng_long = Total_Amt_Chng.melt(id_vars=["Total_Amt_Chng_Q4_Q1_Category", "Total_Ct_Chng_Q4_Q1_Category"], var_name="Attrition_Flag", value_name="Count")

        Total_Amt_Chng_long["Total_Amt_Chng_Q4_Q1_Category"] = pd.Categorical(Total_Amt_Chng_long["Total_Amt_Chng_Q4_Q1_Category"], categories=['Low Amt Change', 'Medium Amt Change', 'High Amt Change', 'Very High Amt Change'], ordered=True)
        Total_Amt_Chng_long["Total_Ct_Chng_Q4_Q1_Category"] = pd.Categorical(Total_Amt_Chng_long["Total_Ct_Chng_Q4_Q1_Category"], categories=['Low Ct Change', 'Medium Ct Change', 'High Ct Change', 'Very High Ct Change'], ordered=True)
        Total_Amt_Chng_long = Total_Amt_Chng_long.sort_values(by=["Total_Ct_Chng_Q4_Q1_Category", "Total_Amt_Chng_Q4_Q1_Category"])
        fig = px.area(Total_Amt_Chng_long, x="Total_Amt_Chng_Q4_Q1_Category", y="Count", color="Attrition_Flag", markers=True, facet_col="Total_Ct_Chng_Q4_Q1_Category",
                    title="Trend of Churn by Amount Change and Count Change", labels={"Total_Amt_Chng_Q4_Q1_Category": "", "Total_Ct_Chng_Q4_Q1_Category": "", "Count": "", "Attrition_Flag": ""},
                    color_discrete_sequence=px.colors.qualitative.Set1)
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', '')))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### b. Total Amount Spend and Total Number of Transactions")
        Total_Trans_Amt_Ct = pd.crosstab(index=[df_churn["Total_Trans_Amt_Category"], df_churn["Total_Trans_Ct_Category"]], columns=df_churn["Attrition_Flag"]).reset_index()
        Total_Trans_Amt_Ct_long = Total_Trans_Amt_Ct.melt(id_vars=["Total_Trans_Amt_Category", "Total_Trans_Ct_Category"], var_name="Attrition_Flag", value_name="Count")
        Total_Trans_Amt_Ct_long["Total_Trans_Amt_Category"] = pd.Categorical(Total_Trans_Amt_Ct_long["Total_Trans_Amt_Category"], categories=["Low Spend", "Medium Spend", "High Spend"], ordered=True)
        Total_Trans_Amt_Ct_long["Total_Trans_Ct_Category"] = pd.Categorical(Total_Trans_Amt_Ct_long["Total_Trans_Ct_Category"], categories=["Low Transactions", "Medium Transactions", "High Transactions"], ordered=True)
        Total_Trans_Amt_Ct_long = Total_Trans_Amt_Ct_long.sort_values(by=["Total_Trans_Ct_Category", "Total_Trans_Amt_Category"])
        fig = px.bar(Total_Trans_Amt_Ct_long, x="Total_Trans_Amt_Category", y="Count", color="Attrition_Flag", facet_col="Total_Trans_Ct_Category", barmode="group", title="Churn Distribution by Transaction Amount & Count Categories",labels={"Total_Trans_Amt_Category": "", "Total_Trans_Ct_Category": "", "Count": "", "Attrition_Flag": ""}, text_auto=True, color_discrete_sequence=px.colors.qualitative.Set1)
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', '')))
        st.plotly_chart(fig, use_container_width=True)    

    with tabs[5]:
        st.markdown("##### a. Card Type and Total Relationship Count")
        card_relationship = pd.crosstab(index=[df_churn["Card_Category"], df_churn["Total_Relationship_Count"]],
                                        columns=df_churn["Attrition_Flag"]).reset_index()
        card_relationship_long = card_relationship.melt(id_vars=["Card_Category", "Total_Relationship_Count"],
                                                        var_name="Attrition_Flag", value_name="Count")
        fig = px.line(card_relationship_long, x="Total_Relationship_Count", y="Count", color="Attrition_Flag", facet_col="Card_Category",markers=True, title="Churn Distribution by Card Category and Total Relationship Count", labels={"Total_Relationship_Count": "", "Count": "", "Attrition_Flag": "", "Card_Category": ""}, color_discrete_map={"Attrited Customer": "red", "Existing Customer": "blue"})
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', '')))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("##### b. Total Inactive Months and Bank Interactions")
        Inactive_Contacts = pd.crosstab([df_churn["Months_Inactive_12_mon"], df_churn["Contacts_Count_12_mon"]],
                                        df_churn["Attrition_Flag"]).reset_index()
        Inactive_Contacts_long = Inactive_Contacts.melt(id_vars=["Months_Inactive_12_mon", "Contacts_Count_12_mon"],
                                                        var_name="Attrition_Flag", value_name="Count")
        fig = px.bar(Inactive_Contacts_long, x="Months_Inactive_12_mon", y="Count", color="Attrition_Flag", barmode="stack", facet_col="Contacts_Count_12_mon", title="Churn Distribution by Months Inactive and Contacts Count",
        labels={"Months_Inactive_12_mon": "Months Inactive", "Count": "", "Attrition_Flag": "", "Contacts_Count_12_mon": "Contacts Month"}, text_auto=True, color_discrete_sequence=px.colors.qualitative.Set1)
        fig.for_each_annotation(lambda a: a.update(text=a.text.replace('=', '')))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Data Displayed")
    st.dataframe(df_churn)

if __name__ == "__main__":
    app()
