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
    iframe { border: none; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Market Share Dashboard")
st.markdown("Real-time data from [StatCounter Global Stats](https://gs.statcounter.com/)")

# ============== Date Calculation ==============
def get_current_end_month():
    """Get the previous month in YYYYMM format"""
    today = datetime.now()
    first_of_month = today.replace(day=1)
    last_month = first_of_month - timedelta(days=1)
    return last_month.strftime("%Y%m")

def get_start_month(category):
    """Get start month based on category"""
    if category == "ai_chatbot":
        return "202503"
    else:
        return "202306"

# ============== Embed Using Full HTML Page ==============
def create_embed_html(chart_type, category, start_month, end_month, width=950, height=450):
    """Create a complete HTML page with StatCounter embed"""
    
    if category == "search_engine":
        chart_id = f"all-search_engine-ww-monthly-{start_month}-{end_month}"
        source_url = f"https://gs.statcounter.com/search-engine-market-share#monthly-{start_month}-{end_month}"
        source_text = "Search Engine Market Share"
    elif category == "os":
        chart_id = f"all-os_combined-ww-monthly-{start_month}-{end_month}"
        source_url = f"https://gs.statcounter.com/os-market-share#monthly-{start_month}-{end_month}"
        source_text = "OS Market Share"
    elif category == "ai_chatbot":
        chart_id = f"all-ai_chatbot-ww-monthly-{start_month}-{end_month}"
        source_url = f"https://gs.statcounter.com/ai-chatbot-market-share#monthly-{start_month}-{end_month}"
        source_text = "AI Chatbot Market Share"
    else:
        return ""
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; padding: 10px; font-family: Arial, sans-serif; background: white; }}
            #chart-container {{ width: {width}px; height: {height}px; }}
            .source {{ font-size: 12px; color: #666; margin-top: 10px; }}
            .source a {{ color: #1a73e8; text-decoration: none; }}
            .source a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div id="{chart_id}" width="{width}" height="{height}" style="width:{width}px; height:{height}px;"></div>
        <p class="source">Source: <a href="{source_url}" target="_blank">StatCounter Global Stats - {source_text}</a></p>
        <script type="text/javascript" src="https://www.statcounter.com/js/fusioncharts.js"></script>
        <script type="text/javascript" src="https://gs.statcounter.com/chart.php?{chart_id}&chartWidth={width}"></script>
    </body>
    </html>
    '''
    return html

# ============== Main Layout ==============

end_month = get_current_end_month()
st.info(f"📅 데이터 기간: 2023-06 ~ {end_month[:4]}-{end_month[4:]} (자동 업데이트)")

# Tabs for different categories
tab1, tab2, tab3 = st.tabs(["🔍 Search Engine", "💻 Operating System", "🤖 AI Chatbot"])

with tab1:
    st.header("Search Engine Market Share")
    st.markdown("Worldwide search engine market share trends")
    
    start_month = get_start_month("search_engine")
    html_content = create_embed_html("chart", "search_engine", start_month, end_month)
    components.html(html_content, height=520, scrolling=False)

with tab2:
    st.header("Operating System Market Share")
    st.markdown("Worldwide OS market share trends (Desktop + Mobile + Tablet + Console)")
    
    start_month = get_start_month("os")
    html_content = create_embed_html("chart", "os", start_month, end_month)
    components.html(html_content, height=520, scrolling=False)

with tab3:
    st.header("AI Chatbot Market Share")
    st.markdown("Worldwide AI chatbot usage trends")
    
    start_month = get_start_month("ai_chatbot")
    html_content = create_embed_html("chart", "ai_chatbot", start_month, end_month)
    components.html(html_content, height=520, scrolling=False)

# Alternative: Direct links if embed doesn't work
st.markdown("---")
st.markdown("### 📎 직접 링크 (차트가 안 보이는 경우)")
col1, col2, col3 = st.columns(3)
with col1:
    se_start = get_start_month("search_engine")
    st.link_button("🔍 Search Engine", f"https://gs.statcounter.com/search-engine-market-share#monthly-{se_start}-{end_month}")
with col2:
    os_start = get_start_month("os")
    st.link_button("💻 OS", f"https://gs.statcounter.com/os-market-share#monthly-{os_start}-{end_month}")
with col3:
    ai_start = get_start_month("ai_chatbot")
    st.link_button("🤖 AI Chatbot", f"https://gs.statcounter.com/ai-chatbot-market-share#monthly-{ai_start}-{end_month}")

# Footer
st.markdown("---")
st.markdown(f"""
<p style='color:gray; font-size:12px;'>
Last updated: {datetime.now().strftime('%Y. %m. %d. %H:%M:%S')} | 
Data automatically refreshes when StatCounter updates
</p>
""", unsafe_allow_html=True)
