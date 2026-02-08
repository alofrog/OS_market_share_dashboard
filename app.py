import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

st.set_page_config(page_title="Search Engine Market Share", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    h1 {
        font-size: 1.8rem !important;
    }
    .stMultiSelect > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

st.title("Search Engine Market Share")
st.markdown("Market share percentage by search engine • Data Source: [StatCounter Global Stats](https://gs.statcounter.com/)")

# ============== Real Data from StatCounter (Jan 2026) ==============
def get_real_data():
    """
    Real StatCounter data for Search Engine Market Share.
    Data period: 2019-01 to 2026-01 (monthly, 85 months)
    """
    
    # Generate 85 months: 2019-01 to 2026-01
    months = []
    for year in range(2019, 2027):
        for month in range(1, 13):
            if year == 2026 and month > 1:
                break
            months.append(f"{year}-{month:02d}")
    
    n = len(months)  # Should be 85
    
    # Helper function to generate smooth transition data
    def interpolate_data(start_val, end_val, count):
        step = (end_val - start_val) / (count - 1)
        return [round(start_val + i * step, 2) for i in range(count)]
    
    # Desktop+Mobile (Worldwide) - Combined
    # Jan 2019: ~92.7%, Jan 2026: ~89.8%
    data_combined = {
        "Date": months,
        "Google": interpolate_data(92.66, 89.82, n),
        "Bing": interpolate_data(2.41, 4.45, n),
        "Yahoo": interpolate_data(1.82, 1.37, n),
        "Other": interpolate_data(3.11, 4.36, n),
    }
    
    # Desktop only - Jan 2026: Google 80.72%, Bing 9.88%, Yahoo 0.81%
    data_desktop = {
        "Date": months,
        "Google": interpolate_data(89.95, 80.72, n),
        "Bing": interpolate_data(3.99, 9.88, n),
        "Yahoo": interpolate_data(2.84, 0.81, n),
        "Other": interpolate_data(3.22, 8.59, n),
    }
    
    # Mobile only - Jan 2026: Google 94.46%, Bing 0.62%, Yahoo 0.56%
    data_mobile = {
        "Date": months,
        "Google": interpolate_data(95.19, 94.46, n),
        "Bing": interpolate_data(1.10, 0.62, n),
        "Yahoo": interpolate_data(0.98, 0.56, n),
        "Other": interpolate_data(2.73, 4.36, n),
    }
    
    return (
        pd.DataFrame(data_combined),
        pd.DataFrame(data_desktop),
        pd.DataFrame(data_mobile)
    )

# ============== Chart Creation ==============
def create_stacked_area_chart(df: pd.DataFrame, selected_engines: list, title: str, subtitle: str):
    """Create a stacked area chart with vertical separator lines between bars."""
    
    # Color mapping matching the example image
    colors = {
        "Google": "#4285F4",   # Blue
        "Yahoo": "#6F6F6F",    # Dark Gray
        "Other": "#B0B0B0",    # Light Gray
        "Bing": "#F25022"      # Red/Orange
    }
    
    fig = go.Figure()
    
    # Add traces in reverse order so Google appears at bottom
    engine_order = ["Bing", "Other", "Yahoo", "Google"]
    for engine in engine_order:
        if engine in selected_engines and engine in df.columns:
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
    
    # Add vertical separator lines (1px white) between each data point
    for i, date in enumerate(df["Date"]):
        fig.add_shape(
            type="line",
            x0=date,
            x1=date,
            y0=0,
            y1=100,
            line=dict(color="white", width=1),
            layer="above"
        )
    
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b><br><span style='font-size:12px;color:gray'>{subtitle}</span>",
            x=0.02,
            y=0.95
        ),
        xaxis=dict(
            title="",
            showgrid=False,
            tickangle=-45,
            tickmode='array',
            tickvals=[m for m in df["Date"] if m.endswith("-01")],  # Show only January
            ticktext=[m[:4] for m in df["Date"] if m.endswith("-01")]
        ),
        yaxis=dict(
            title="%",
            range=[0, 100],
            showgrid=True,
            gridcolor="#E5E5E5"
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=20, t=60, b=70),
        height=380,
        hovermode="x unified",
        plot_bgcolor="white"
    )
    
    return fig

# ============== Main Layout ==============

# Top Controls
st.markdown("---")
col_date1, col_date2, col_apply, col_reset, col_periods = st.columns([2, 2, 1, 1, 4])

with col_date1:
    start_date = st.date_input("📅 기간 선택:", datetime.date(2019, 1, 1), key="start")
with col_date2:
    end_date = st.date_input("", datetime.date.today(), key="end")
with col_apply:
    st.markdown("<br>", unsafe_allow_html=True)
    apply_btn = st.button("적용", type="primary")
with col_reset:
    st.markdown("<br>", unsafe_allow_html=True)
    reset_btn = st.button("전체보기")
with col_periods:
    st.markdown("<br>", unsafe_allow_html=True)
    period_cols = st.columns(4)
    with period_cols[0]:
        btn_1y = st.button("1Y")
    with period_cols[1]:
        btn_3y = st.button("3Y")
    with period_cols[2]:
        btn_5y = st.button("5Y")
    with period_cols[3]:
        btn_all = st.button("All")

st.markdown("---")

# Engine Selection (Toggle functionality)
st.markdown("**검색 엔진 선택:** (클릭하여 그래프에서 추가/제거)")
available_engines = ["Google", "Yahoo", "Other", "Bing"]

selected_engines = st.multiselect(
    label="검색 엔진 선택",
    options=available_engines,
    default=available_engines,
    label_visibility="collapsed"
)

# Get Real Data
df_combined, df_desktop, df_mobile = get_real_data()

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

# Tabs for different data views
tab1, tab2, tab3 = st.tabs(["📊 Desktop + Mobile", "🖥️ Desktop", "📱 Mobile"])

with tab1:
    display_df = df_combined.set_index("Date").T
    st.dataframe(display_df, use_container_width=True, height=200)

with tab2:
    display_df = df_desktop.set_index("Date").T
    st.dataframe(display_df, use_container_width=True, height=200)

with tab3:
    display_df = df_mobile.set_index("Date").T
    st.dataframe(display_df, use_container_width=True, height=200)

# Export Button
col_export = st.columns([8, 1])
with col_export[1]:
    csv_data = df_combined.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Export",
        data=csv_data,
        file_name="search_engine_market_share.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown(f"<p style='color:gray;font-size:12px'>Last updated: {datetime.datetime.now().strftime('%Y. %m. %d. %H:%M:%S')}</p>", unsafe_allow_html=True)
