import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(page_title="Market Share Dashboard", layout="wide")

st.markdown("""
<style>
    .main > div { padding-top: 1rem; }
    .block-container { padding-top: 1rem; }
    h1 { font-size: 2rem !important; font-weight: bold; }
    iframe { border: 1px solid #ddd; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Market Share Dashboard")
st.markdown("Real-time data from [StatCounter Global Stats](https://gs.statcounter.com/)")

# ============== Date Calculation ==============
def get_current_end_month():
    today = datetime.now()
    first_of_month = today.replace(day=1)
    last_month = first_of_month - timedelta(days=1)
    return last_month.strftime("%Y%m")

end_month = get_current_end_month()
st.info(f"📅 데이터 기간 종료: {end_month[:4]}-{end_month[4:]}")

# ============== Tabs ==============
tab1, tab2, tab3 = st.tabs(["🔍 Search Engine", "💻 Operating System", "🤖 AI Chatbot"])

with tab1:
    st.header("Search Engine Market Share")
    # Embed StatCounter page directly via iframe
    iframe_url = f"https://gs.statcounter.com/search-engine-market-share/all/worldwide/chart.php?bar=1&device=Desktop%20%26%20Mobile&device_hidden=desktop%2Bmobile&multi=1&period=monthly&statType_hidden=search_engine&region_hidden=ww&granularity=monthly&statType=Search%20Engine&region=Worldwide&fromInt=202306&toInt={end_month}&fromMonthYear=2023-06&toMonthYear={end_month[:4]}-{end_month[4:]}&csv=1"
    
    st.markdown(f"""
    <iframe src="https://gs.statcounter.com/search-engine-market-share#monthly-202306-{end_month}" 
            width="100%" height="600" style="border:1px solid #ccc; border-radius:8px;">
    </iframe>
    """, unsafe_allow_html=True)
    
    st.link_button("🔗 StatCounter에서 직접 보기", f"https://gs.statcounter.com/search-engine-market-share#monthly-202306-{end_month}")

with tab2:
    st.header("Operating System Market Share")
    st.markdown(f"""
    <iframe src="https://gs.statcounter.com/os-market-share#monthly-202306-{end_month}" 
            width="100%" height="600" style="border:1px solid #ccc; border-radius:8px;">
    </iframe>
    """, unsafe_allow_html=True)
    
    st.link_button("🔗 StatCounter에서 직접 보기", f"https://gs.statcounter.com/os-market-share#monthly-202306-{end_month}")

with tab3:
    st.header("AI Chatbot Market Share")
    st.markdown(f"""
    <iframe src="https://gs.statcounter.com/ai-chatbot-market-share#monthly-202503-{end_month}" 
            width="100%" height="600" style="border:1px solid #ccc; border-radius:8px;">
    </iframe>
    """, unsafe_allow_html=True)
    
    st.link_button("🔗 StatCounter에서 직접 보기", f"https://gs.statcounter.com/ai-chatbot-market-share#monthly-202503-{end_month}")

st.markdown("---")
st.markdown("### 📄 로컬에서 차트 보기")
st.markdown("StatCounter iframe이 안 보이는 경우, `charts.html` 파일을 브라우저에서 직접 열어보세요.")

st.markdown(f"""
<p style='color:gray; font-size:12px;'>
Last updated: {datetime.now().strftime('%Y. %m. %d. %H:%M:%S')}
</p>
""", unsafe_allow_html=True)
