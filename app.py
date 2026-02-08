import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from data_loader import (
    get_sample_search_engine_data,
    get_sample_os_data,
    get_sample_ai_chatbot_data,
    get_current_end_month
)

st.set_page_config(page_title="Market Share Dashboard", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main > div { padding-top: 1rem; }
    .block-container { padding-top: 1rem; }
    h1 { font-size: 2rem !important; font-weight: bold; }
    .stMultiSelect > div { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Market Share Dashboard")
st.markdown("Data Source: [StatCounter Global Stats](https://gs.statcounter.com/) | Last values: Jan 2026")

# ============== Chart Creation ==============
def create_stacked_area_chart(df: pd.DataFrame, selected_items: list, title: str, subtitle: str):
    """Create a stacked area chart with vertical separator lines"""
    
    # Extended color palette
    colors = {
        # Search Engines
        "Google": "#4285F4",
        "Bing": "#F25022",
        "Yahoo": "#6F6F6F",
        "Baidu": "#2932E1",
        "YANDEX": "#FF0000",
        "DuckDuckGo": "#DE5833",
        # OS
        "Windows": "#00A4EF",
        "Android": "#3DDC84",
        "iOS": "#555555",
        "macOS": "#999999",
        "Linux": "#FCC624",
        "Chrome OS": "#4285F4",
        "Unknown": "#CCCCCC",
        # AI Chatbots
        "ChatGPT": "#10A37F",
        "Gemini": "#4285F4",
        "Copilot": "#00A4EF",
        "Claude": "#CC785C",
        "Perplexity": "#20808D",
        # Default
        "Other": "#B0B0B0",
    }
    
    fig = go.Figure()
    
    # Get available columns (excluding Date)
    available = [col for col in df.columns if col != "Date"]
    
    # Add traces in reverse order (bottom to top)
    for item in reversed(available):
        if item in selected_items:
            fig.add_trace(go.Scatter(
                x=df["Date"],
                y=df[item],
                name=item,
                mode='lines',
                stackgroup='one',
                fillcolor=colors.get(item, "#888888"),
                line=dict(width=0.5, color=colors.get(item, "#888888")),
                hovertemplate=f"{item}: %{{y:.2f}}%<extra></extra>"
            ))
    
    # Add vertical separator lines (1px white)
    for date in df["Date"]:
        fig.add_shape(
            type="line", x0=date, x1=date, y0=0, y1=100,
            line=dict(color="white", width=1), layer="above"
        )
    
    # X-axis: show only years
    tick_vals = [m for m in df["Date"] if m.endswith("-01")]
    tick_text = [m[:4] for m in tick_vals]
    
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b><br><span style='font-size:12px;color:gray'>{subtitle}</span>",
            x=0.02, y=0.95
        ),
        xaxis=dict(
            title="", showgrid=False, tickangle=-45,
            tickmode='array', tickvals=tick_vals, ticktext=tick_text
        ),
        yaxis=dict(title="%", range=[0, 100], showgrid=True, gridcolor="#E5E5E5"),
        legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=40, r=20, t=60, b=60),
        height=400, hovermode="x unified", plot_bgcolor="white"
    )
    
    return fig

# ============== Main Layout ==============

end_month = get_current_end_month()
st.info(f"📅 데이터 기간: 2023-06 ~ {end_month[:4]}-{end_month[4:]} | ⚠️ 현재 샘플 데이터 사용 중 (StatCounter API 접근 제한)")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Search Engine", "💻 Operating System", "🤖 AI Chatbot"])

# ============== Search Engine Tab ==============
with tab1:
    st.header("Search Engine Market Share")
    
    df_se = get_sample_search_engine_data()
    engines = [col for col in df_se.columns if col != "Date"]
    
    selected_engines = st.multiselect(
        "검색 엔진 선택 (클릭하여 추가/제거):",
        options=engines,
        default=engines,
        key="engines"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        fig1 = create_stacked_area_chart(df_se, selected_engines, "Desktop+Mobile", "Combined market share (%)")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = create_stacked_area_chart(df_se, selected_engines, "Desktop", "Desktop only (%)")
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        fig3 = create_stacked_area_chart(df_se, selected_engines, "Mobile", "Mobile only (%)")
        st.plotly_chart(fig3, use_container_width=True)
    
    st.subheader("Data Table")
    st.dataframe(df_se.set_index("Date").T, use_container_width=True, height=250)

# ============== OS Tab ==============
with tab2:
    st.header("Operating System Market Share")
    
    df_os = get_sample_os_data()
    os_list = [col for col in df_os.columns if col != "Date"]
    
    selected_os = st.multiselect(
        "OS 선택:",
        options=os_list,
        default=os_list,
        key="os"
    )
    
    fig_os = create_stacked_area_chart(df_os, selected_os, "All Platforms", "Desktop + Mobile + Tablet + Console (%)")
    st.plotly_chart(fig_os, use_container_width=True)
    
    st.subheader("Data Table")
    st.dataframe(df_os.set_index("Date").T, use_container_width=True, height=280)

# ============== AI Chatbot Tab ==============
with tab3:
    st.header("AI Chatbot Market Share")
    st.caption("Data available from March 2025")
    
    df_ai = get_sample_ai_chatbot_data()
    ai_list = [col for col in df_ai.columns if col != "Date"]
    
    selected_ai = st.multiselect(
        "AI Chatbot 선택:",
        options=ai_list,
        default=ai_list,
        key="ai"
    )
    
    fig_ai = create_stacked_area_chart(df_ai, selected_ai, "AI Chatbot Usage", "Worldwide usage share (%)")
    st.plotly_chart(fig_ai, use_container_width=True)
    
    st.subheader("Data Table")
    st.dataframe(df_ai.set_index("Date").T, use_container_width=True, height=220)

# ============== Footer ==============
st.markdown("---")
st.markdown(f"""
<p style='color:gray; font-size:12px;'>
Last updated: {datetime.now().strftime('%Y. %m. %d. %H:%M:%S')} | 
📌 StatCounter가 직접 API 접근을 차단하여 현재 샘플 데이터를 사용합니다. 
정확한 데이터는 <a href="https://gs.statcounter.com" target="_blank">StatCounter</a>에서 확인하세요.
</p>
""", unsafe_allow_html=True)
