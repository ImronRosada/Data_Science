import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📊 Zomato Delivery Time Operation Dashboard")

    # Load dataset
    df_zomato = pd.read_csv("Zomato_Delivery_Time/dataset/df_zomato_dashboard.csv")

    # Sidebar filters
    st.sidebar.header("🔍 Filter Options")
    city_opts = df_zomato['City'].dropna().unique()
    city_filter = st.sidebar.multiselect("City Category:", city_opts, default=city_opts)

    speed_filter = []
    for option in df_zomato['delivery_speed_category'].dropna().unique():
        if st.sidebar.checkbox(option, True, key=f"speed_{option}"):
            speed_filter.append(option)

    weather_opts = df_zomato['Weather_conditions'].dropna().unique()
    weather_filter = st.sidebar.multiselect("Weather Conditions:", weather_opts, default=weather_opts)

    traffic_opts = df_zomato['Road_traffic_density'].dropna().unique()
    traffic_filter = st.sidebar.multiselect("Traffic Density:", traffic_opts, default=traffic_opts)

    df_zomato['Order_Date'] = pd.to_datetime(df_zomato['Order_Date'])
    min_date = df_zomato['Order_Date'].min()
    max_date = df_zomato['Order_Date'].max()
    date_filter = st.sidebar.date_input("Order Date Range:", [min_date, max_date], min_value=min_date, max_value=max_date)

    if date_filter and len(date_filter) == 2:
        start_date, end_date = pd.to_datetime(date_filter[0]), pd.to_datetime(date_filter[1])
    else:
        st.warning("⚠️ Please select a valid date range.")
        return

    # Apply filters
    df = df_zomato[
        df_zomato['City'].isin(city_filter) &
        df_zomato['delivery_speed_category'].isin(speed_filter) &
        df_zomato['Weather_conditions'].isin(weather_filter) &
        df_zomato['Road_traffic_density'].isin(traffic_filter) &
        df_zomato['Order_Date'].between(start_date, end_date)
    ]

    if df.empty:
        st.warning("⚠️ No data found for the selected filters. Please adjust the filters to see the data.")
        return

    # Tabs layout
    tabs = st.tabs([
        "⏱️ Time Distribution",
        "🚀 Speed Categories",
        "📈 Avg Speed by Category",
        "🌦️ Weather & Traffic",
        "⏳ Distance vs Time",
        "🗓️ Time & Orders",
        "⭐ Courier Performance"
    ])

    with tabs[0]:
        st.subheader("⏱️ Delivery Time Distribution")
        basic_stats = df["Time_taken (min)"].describe().to_frame().T
        fig = px.histogram(df, x='Time_taken (min)', nbins=40, color_discrete_sequence=px.colors.qualitative.T10, text_auto=True)
        fig.update_layout(title="Distribution of Delivery Time (min)", xaxis_title="Time Taken (min)", yaxis_title="", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(basic_stats)

    with tabs[1]:
        st.subheader("🚀 Delivery Speed Category Distribution")
        basic_stats = df.groupby('delivery_speed_category', observed=True)['Time_taken (min)'].describe()
        speed_dist = df['delivery_speed_category'].value_counts().reset_index()
        speed_dist.columns = ['Category', 'Count']
        speed_dist['Percentage (%)'] = round(speed_dist['Count'] / speed_dist['Count'].sum() * 100, 2)
        fig = px.pie(speed_dist, names='Category', values='Count', hole=0.4, title="Distribution of Delivery Categories", color_discrete_sequence=px.colors.qualitative.T10)
        fig.update_traces(textposition='inside', textinfo='percent+label+value')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(basic_stats)

    with tabs[2]:
        st.subheader("📈 Average Speed by Category")
        avg_speed = df.groupby('delivery_speed_category', observed=True)['Speed_kmph'].mean().round(2).reset_index()
        avg_speed.columns = ['Delivery Speed Category', 'Average Speed (km/h)']
        df['Speed_kmph'] = pd.to_numeric(df['Speed_kmph'], errors='coerce')
        fig = px.histogram(df, x='Speed_kmph', color='delivery_speed_category', barmode="stack", nbins=24, text_auto=True,
                           title='Distribution of Delivery Speed (Fast vs Slow)',
                           labels={'Speed_kmph': 'Speed (km/h)', 'delivery_speed_category': ''},
                           color_discrete_sequence=px.colors.qualitative.T10)
        fig.update_layout(showlegend=True, xaxis_title="Speed (km/h)", yaxis_title="", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(avg_speed.T)

    with tabs[3]:
        st.subheader("🌦️ Impact of Weather and Traffic")
        grouped = df.groupby(['Weather_conditions', 'Road_traffic_density'])['Time_taken (min)'].mean().reset_index()
        fig = px.density_heatmap(grouped, x='Road_traffic_density', y='Weather_conditions', z='Time_taken (min)', text_auto='.1f',
                                 category_orders={'Road_traffic_density': ['Low', 'Medium', 'High', 'Very High']},
                                 color_continuous_scale='Cividis')
        fig.update_layout(title='Avg Delivery Time by Weather and Traffic', height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(grouped.T)

    with tabs[4]:
        st.subheader("⏳ Distance vs Delivery Time")
        distance_avg = df.groupby('distance_km')['Time_taken (min)'].mean().reset_index()
        fig = px.area(distance_avg, x='distance_km', y='Time_taken (min)', title="Avg Delivery Time by Distance")
        fig.update_traces(line_color='royalblue', fillcolor='rgba(65,105,225,0.3)')
        min_idx = distance_avg['Time_taken (min)'].idxmin()
        fig.add_scatter(x=[distance_avg.loc[min_idx, 'distance_km']], y=[distance_avg.loc[min_idx, 'Time_taken (min)']],
                        mode='markers', marker=dict(color='green', size=10), name='Fast Delivery')
        max_idx = distance_avg['Time_taken (min)'].idxmax()
        fig.add_scatter(x=[distance_avg.loc[max_idx, 'distance_km']], y=[distance_avg.loc[max_idx, 'Time_taken (min)']],
                        mode='markers', marker=dict(color='red', size=10), name='Slow Delivery')
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(distance_avg.T)

    with tabs[5]:
        st.subheader("🗓️ Delivery Time by Order Date")
        hourly_daily = df.groupby(["day_of_week", "hour_of_day"])["Time_taken (min)"].mean().reset_index()
        hourly_daily.columns = ["day_of_week", "hour_of_day", "avg_time_taken"]
        day_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        hourly_daily["day_of_week"] = hourly_daily["day_of_week"].map(day_map)
        fig = px.line(hourly_daily, x="hour_of_day", y="avg_time_taken", color="day_of_week", markers=True,
                      title="Hour and Day of Order", labels={"hour_of_day": "Order Hour", "avg_time_taken": "Avg Duration (min)"})
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(hourly_daily.T)

        combined = df.groupby(["day_of_week", "hour_of_day"]).agg(order_count=("Time_taken (min)", "count")).reset_index()
        combined["day_of_week"] = combined["day_of_week"].map(day_map)
        fig2 = px.line(combined, x="hour_of_day", y="order_count", color="day_of_week", markers=True,
                       title="Hour and Day (Busy Time)", labels={"order_count": "Order Count"})
        fig2.update_layout(template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(combined.T)

    with tabs[6]:
        st.subheader("⭐ Courier Performance Distribution")
        perf = df.groupby(["Delivery_person_Ratings", "Vehicle_condition"])["Time_taken (min)"].agg(avg_time_taken="mean", order_count="count").reset_index()
        fig = px.bar(perf, x="Delivery_person_Ratings", y="avg_time_taken", color="Delivery_person_Ratings",
                     facet_col="Vehicle_condition", category_orders={"Vehicle_condition": [0, 1, 2, 3]},
                     title="Avg Delivery Time by Rating & Vehicle Condition",
                     labels={"Delivery_person_Ratings": "Courier Rating", "avg_time_taken": "Avg Time (min)"})
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(perf.T)

    # Final data display
    st.markdown("#### 📋 Data Displayed")
    st.dataframe(df)

