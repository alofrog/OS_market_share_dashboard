import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from data_loader import get_statcounter_data, get_mock_data

st.set_page_config(page_title="Market Share Dashboard", layout="wide")

st.title("Search Engine & OS Market Share")
st.markdown("Data Source: [StatCounter Global Stats](https://gs.statcounter.com/)")

# Sidebar Controls
st.sidebar.header("Configuration")

category = st.sidebar.selectbox(
    "Category",
    ["Search Engine", "Operating System", "Browser"]
)

# Map category to metric code
metric_map = {
    "Search Engine": "search_engine",
    "Operating System": "os",
    "Browser": "browser"
}
metric = metric_map[category]

device = st.sidebar.selectbox(
    "Device",
    ["Desktop", "Mobile", "Tablet", "Console", "Combined"]
)
device_code = device.lower()

# Date Range
today = datetime.date.today()
start_date = st.sidebar.date_input("Start Date", today - datetime.timedelta(days=365))
end_date = st.sidebar.date_input("End Date", today)

# Fetch Data
if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data from StatCounter..."):
        # We need to handle the date format expected by StatCounter (Monthly)
        # Verify dates
        if start_date > end_date:
            st.error("Start date must be before end date.")
        else:
            df = get_statcounter_data(metric, device_code, "ww", start_date, end_date)
            
            if df is None:
                st.warning("Failed to fetch live data. Loading mock data for demonstration.")
                df = get_mock_data()
            
            st.session_state['data'] = df
            st.session_state['data_params'] = f"{category} - {device}"

# Display Data
if 'data' in st.session_state:
    df = st.session_state['data']
    st.header(f"Market Share: {st.session_state.get('data_params', '')}")
    
    # Process Data for Plotting
    # StatCounter CSV usually has 'Date' column and then columns for each item with values.
    # We might need to melt key columns if we want to toggle them, or Plotly handles it.
    
    # Verify 'Date' column exists or find the time column
    time_col = df.columns[0] # Usually first column
    
    # Create Line Chart
    fig = px.line(df, x=time_col, y=df.columns[1:], title=f"{category} Market Share (%)", markers=True)
    fig.update_layout(hovermode="x unified", xaxis_title="Date", yaxis_title="Market Share (%)")
    fig.update_yaxes(range=[0, 100])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    st.subheader("Data Table")
    st.dataframe(df, use_container_width=True)
    
    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name='market_share_data.csv',
        mime='text/csv',
    )
else:
    st.info("Please select parameters and click 'Fetch Data' to verify.")
