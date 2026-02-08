import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Search Engine Market Share", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main > div { padding-top: 1rem; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    h1 { font-size: 1.8rem !important; }
    .stMultiSelect > div { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

st.title("Search Engine Market Share")
st.markdown("Market share percentage by search engine • Data Source: [StatCounter Global Stats](https://gs.statcounter.com/)")

# ============== Data Loading ==============
def get_default_data():
    """Default placeholder data (will be replaced by uploaded CSV)"""
    months = []
    for year in range(2019, 2027):
        for month in range(1, 13):
            if year == 2026 and month > 1:
                break
            months.append(f"{year}-{month:02d}")
    
    n = len(months)
    
    def interp(start, end, count):
        return [round(start + i * (end - start) / (count - 1), 2) for i in range(count)]
    
    data_combined = pd.DataFrame({
        "Date": months,
        "Google": interp(92.66, 89.82, n),
        "Bing": interp(2.41, 4.45, n),
        "Yahoo": interp(1.82, 1.37, n),
        "Other": interp(3.11, 4.36, n),
    })
    
    data_desktop = pd.DataFrame({
        "Date": months,
        "Google": interp(89.95, 80.72, n),
        "Bing": interp(3.99, 9.88, n),
        "Yahoo": interp(2.84, 0.81, n),
        "Other": interp(3.22, 8.59, n),
    })
    
    data_mobile = pd.DataFrame({
        "Date": months,
        "Google": interp(95.19, 94.46, n),
        "Bing": interp(1.10, 0.62, n),
        "Yahoo": interp(0.98, 0.56, n),
        "Other": interp(2.73, 4.36, n),
    })
    
    return data_combined, data_desktop, data_mobile

def parse_uploaded_csv(uploaded_file):
    """Parse uploaded StatCounter CSV file"""
    try:
        df = pd.read_csv(uploaded_file)
        # StatCounter CSV format: First column is Date, rest are search engines
        return df
    except Exception as e:
        st.error(f"CSV 파싱 오류: {e}")
        return None

# ============== Chart Creation ==============
def create_stacked_area_chart(df: pd.DataFrame, selected_engines: list, title: str, subtitle: str):
    """Create a stacked area chart with vertical separator lines."""
    
    colors = {
        "Google": "#4285F4",
        "Yahoo": "#6F6F6F",
        "Other": "#B0B0B0",
        "Bing": "#F25022",
        "YANDEX": "#FF0000",
        "Baidu": "#2932E1",
        "DuckDuckGo": "#DE5833",
    }
    
    fig = go.Figure()
    
    # Get available engines from dataframe (excluding Date column)
    available_in_df = [col for col in df.columns if col != "Date"]
    
    # Add traces in reverse order so first engine appears at bottom
    for engine in reversed(available_in_df):
        if engine in selected_engines:
            fig.add_trace(go.Scatter(
                x=df["Date"],
                y=df[engine],
                name=engine,
                mode='lines',
                stackgroup='one',
                fillcolor=colors.get(engine, "#888888"),
                line=dict(width=0.5, color=colors.get(engine, "#888888")),
                hovertemplate=f"{engine}: %{{y:.2f}}%<extra></extra>"
            ))
    
    # Add vertical separator lines (1px white)
    for date in df["Date"]:
        fig.add_shape(
            type="line", x0=date, x1=date, y0=0, y1=100,
            line=dict(color="white", width=1), layer="above"
        )
    
    # X-axis tick labels (show only years)
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
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        margin=dict(l=40, r=20, t=60, b=70),
        height=380, hovermode="x unified", plot_bgcolor="white"
    )
    
    return fig

# ============== Sidebar: CSV Upload ==============
st.sidebar.header("📁 데이터 업로드")
st.sidebar.markdown("""
**정확한 데이터를 사용하려면:**
1. [StatCounter](https://gs.statcounter.com/chart.php?search_engine-ww-monthly-201901-202601) 방문
2. 차트 아래 **CSV 다운로드** 클릭
3. 아래에 파일 업로드
""")

uploaded_combined = st.sidebar.file_uploader("Desktop+Mobile CSV", type=['csv'], key='combined')
uploaded_desktop = st.sidebar.file_uploader("Desktop CSV", type=['csv'], key='desktop')
uploaded_mobile = st.sidebar.file_uploader("Mobile CSV", type=['csv'], key='mobile')

# Load data (uploaded or default)
if uploaded_combined is not None:
    df_combined = parse_uploaded_csv(uploaded_combined)
    if df_combined is None:
        df_combined, _, _ = get_default_data()
else:
    df_combined, _, _ = get_default_data()

if uploaded_desktop is not None:
    df_desktop = parse_uploaded_csv(uploaded_desktop)
    if df_desktop is None:
        _, df_desktop, _ = get_default_data()
else:
    _, df_desktop, _ = get_default_data()

if uploaded_mobile is not None:
    df_mobile = parse_uploaded_csv(uploaded_mobile)
    if df_mobile is None:
        _, _, df_mobile = get_default_data()
else:
    _, _, df_mobile = get_default_data()

# ============== Main Layout ==============
st.markdown("---")

# Date Range Controls
col_date1, col_date2, col_apply, col_reset, col_periods = st.columns([2, 2, 1, 1, 4])

with col_date1:
    start_date = st.date_input("📅 기간 선택:", datetime.date(2019, 1, 1), key="start")
with col_date2:
    end_date = st.date_input("", datetime.date.today(), key="end")
with col_apply:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("적용", type="primary")
with col_reset:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("전체보기")
with col_periods:
    st.markdown("<br>", unsafe_allow_html=True)
    pcols = st.columns(4)
    with pcols[0]: st.button("1Y")
    with pcols[1]: st.button("3Y")
    with pcols[2]: st.button("5Y")
    with pcols[3]: st.button("All")

st.markdown("---")

# Engine Selection
st.markdown("**검색 엔진 선택:** (클릭하여 그래프에서 추가/제거)")

# Get all available engines from all dataframes
all_engines = set()
for df in [df_combined, df_desktop, df_mobile]:
    all_engines.update([col for col in df.columns if col != "Date"])
all_engines = sorted(list(all_engines))

selected_engines = st.multiselect(
    label="검색 엔진 선택",
    options=all_engines,
    default=all_engines,
    label_visibility="collapsed"
)

# Three Charts Side by Side
chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    fig1 = create_stacked_area_chart(df_combined, selected_engines, "Desktop+Mobile", "Combined market share (%)")
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    fig2 = create_stacked_area_chart(df_desktop, selected_engines, "Desktop", "Desktop only (%)")
    st.plotly_chart(fig2, use_container_width=True)

with chart_col3:
    fig3 = create_stacked_area_chart(df_mobile, selected_engines, "Mobile", "Mobile only (%)")
    st.plotly_chart(fig3, use_container_width=True)

# Data Tables Section
st.markdown("---")
st.subheader("Data Table")
st.markdown("Detailed market share data")

tab1, tab2, tab3 = st.tabs(["📊 Desktop + Mobile", "🖥️ Desktop", "📱 Mobile"])

with tab1:
    st.dataframe(df_combined.set_index("Date").T, use_container_width=True, height=200)
with tab2:
    st.dataframe(df_desktop.set_index("Date").T, use_container_width=True, height=200)
with tab3:
    st.dataframe(df_mobile.set_index("Date").T, use_container_width=True, height=200)

# Export Button
col_export = st.columns([8, 1])
with col_export[1]:
    csv_data = df_combined.to_csv(index=False).encode('utf-8')
    st.download_button(label="⬇️ Export", data=csv_data, file_name="search_engine_market_share.csv", mime="text/csv")

# Footer
st.markdown("---")
st.markdown(f"<p style='color:gray;font-size:12px'>Last updated: {datetime.datetime.now().strftime('%Y. %m. %d. %H:%M:%S')}</p>", unsafe_allow_html=True)
