import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="Market Share Dashboard", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main > div { padding-top: 1rem; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    h1 { font-size: 2rem !important; font-weight: bold; }
    h2 { font-size: 1.5rem !important; margin-top: 1rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Market Share Dashboard")
st.markdown("Real-time data from [StatCounter Global Stats](https://gs.statcounter.com/)")

# ============== Date Calculation ==============
def get_current_end_month():
    """Get the previous month in YYYYMM format (StatCounter data is delayed by ~1 month)"""
    today = datetime.now()
    # Use previous month since current month data is incomplete
    first_of_month = today.replace(day=1)
    last_month = first_of_month - timedelta(days=1)
    return last_month.strftime("%Y%m")

def get_start_month(category):
    """Get start month based on category"""
    if category == "ai_chatbot":
        return "202503"  # AI Chatbot data starts from March 2025
    else:
        return "202306"  # Search Engine and OS data available from June 2023

# ============== HTML Embed Generators ==============
def generate_search_engine_embed(width=600, height=400):
    """Generate Search Engine Market Share embed HTML"""
    end_month = get_current_end_month()
    start_month = get_start_month("search_engine")
    
    html = f'''
    <div id="all-search_engine-ww-monthly-{start_month}-{end_month}" width="{width}" height="{height}" style="width:{width}px; height: {height}px;"></div>
    <p style="font-size:12px; color:gray;">Source: <a href="https://gs.statcounter.com/search-engine-market-share#monthly-{start_month}-{end_month}" target="_blank">StatCounter Global Stats - Search Engine Market Share</a></p>
    <script type="text/javascript" src="https://www.statcounter.com/js/fusioncharts.js"></script>
    <script type="text/javascript" src="https://gs.statcounter.com/chart.php?all-search_engine-ww-monthly-{start_month}-{end_month}&chartWidth={width}"></script>
    '''
    return html

def generate_os_embed(width=600, height=400):
    """Generate OS Market Share embed HTML"""
    end_month = get_current_end_month()
    start_month = get_start_month("os")
    
    html = f'''
    <div id="all-os_combined-ww-monthly-{start_month}-{end_month}" width="{width}" height="{height}" style="width:{width}px; height: {height}px;"></div>
    <p style="font-size:12px; color:gray;">Source: <a href="https://gs.statcounter.com/os-market-share#monthly-{start_month}-{end_month}" target="_blank">StatCounter Global Stats - OS Market Share</a></p>
    <script type="text/javascript" src="https://www.statcounter.com/js/fusioncharts.js"></script>
    <script type="text/javascript" src="https://gs.statcounter.com/chart.php?all-os_combined-ww-monthly-{start_month}-{end_month}&chartWidth={width}"></script>
    '''
    return html

def generate_ai_chatbot_embed(width=600, height=400):
    """Generate AI Chatbot Market Share embed HTML"""
    end_month = get_current_end_month()
    start_month = get_start_month("ai_chatbot")
    
    html = f'''
    <div id="all-ai_chatbot-ww-monthly-{start_month}-{end_month}" width="{width}" height="{height}" style="width:{width}px; height: {height}px;"></div>
    <p style="font-size:12px; color:gray;">Source: <a href="https://gs.statcounter.com/ai-chatbot-market-share#monthly-{start_month}-{end_month}" target="_blank">StatCounter Global Stats - AI Chatbot Market Share</a></p>
    <script type="text/javascript" src="https://www.statcounter.com/js/fusioncharts.js"></script>
    <script type="text/javascript" src="https://gs.statcounter.com/chart.php?all-ai_chatbot-ww-monthly-{start_month}-{end_month}&chartWidth={width}"></script>
    '''
    return html

# ============== Main Layout ==============

# Display current data range
end_month = get_current_end_month()
st.info(f"📅 데이터 기간: 2023-06 ~ {end_month[:4]}-{end_month[4:]} (자동 업데이트)")

# Tabs for different categories
tab1, tab2, tab3 = st.tabs(["🔍 Search Engine", "💻 Operating System", "🤖 AI Chatbot"])

with tab1:
    st.header("Search Engine Market Share")
    st.markdown("Worldwide search engine market share trends")
    
    # Embed StatCounter chart
    components.html(generate_search_engine_embed(width=1000, height=450), height=500)

with tab2:
    st.header("Operating System Market Share")
    st.markdown("Worldwide OS market share trends (Desktop + Mobile + Tablet + Console)")
    
    # Embed StatCounter chart
    components.html(generate_os_embed(width=1000, height=450), height=500)

with tab3:
    st.header("AI Chatbot Market Share")
    st.markdown("Worldwide AI chatbot usage trends")
    
    # Embed StatCounter chart
    components.html(generate_ai_chatbot_embed(width=1000, height=450), height=500)

# Footer
st.markdown("---")
st.markdown(f"""
<p style='color:gray; font-size:12px;'>
Last updated: {datetime.now().strftime('%Y. %m. %d. %H:%M:%S')} | 
Data automatically refreshes when StatCounter updates their charts
</p>
""", unsafe_allow_html=True)
