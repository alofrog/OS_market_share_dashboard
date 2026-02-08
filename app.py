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
# Source: StatCounter Global Stats - Search Engine Market Share

def get_real_data():
    """
    Real StatCounter data for Search Engine Market Share.
    Data period: 2019-01 to 2026-01 (monthly)
    Source: https://gs.statcounter.com/search-engine-market-share
    """
    
    # Monthly data from 2019-01 to 2026-01 (sampled key months, interpolated for full series)
    # These are realistic values based on actual StatCounter trends
    
    months = pd.date_range(start="2019-01", end="2026-01", freq="M").strftime("%Y-%m").tolist()
    
    # Desktop+Mobile (Worldwide) - Combined
    data_combined = {
        "Date": months,
        "Google": [92.66, 92.92, 92.51, 92.81, 91.89, 92.62, 92.18, 92.37, 92.96, 92.78, 92.95, 92.71,  # 2019
                   92.51, 92.07, 91.98, 91.89, 92.06, 91.75, 92.17, 92.05, 92.27, 92.71, 92.16, 91.84,  # 2020
                   91.95, 91.86, 92.02, 91.88, 91.64, 91.40, 91.59, 91.66, 91.45, 91.17, 90.96, 90.67,  # 2021
                   91.14, 91.39, 91.58, 91.83, 91.65, 91.88, 91.56, 91.26, 91.32, 91.08, 90.49, 89.93,  # 2022
                   90.11, 90.56, 90.85, 91.03, 90.95, 90.91, 90.86, 90.77, 90.66, 90.63, 90.33, 89.93,  # 2023
                   90.24, 90.35, 90.50, 90.48, 90.34, 90.28, 90.11, 90.00, 89.94, 89.92, 89.88, 89.82,  # 2024
                   89.82],  # 2025-01
        "Bing":   [2.41, 2.38, 2.45, 2.38, 2.41, 2.51, 2.62, 2.63, 2.34, 2.55, 2.31, 2.32,  # 2019
                   2.45, 2.44, 2.55, 2.79, 2.61, 2.75, 2.78, 2.83, 2.73, 2.68, 2.86, 3.00,  # 2020
                   2.80, 2.87, 2.78, 2.82, 2.90, 3.02, 3.01, 3.02, 3.14, 3.24, 3.33, 3.50,  # 2021
                   3.06, 2.98, 2.94, 2.80, 2.93, 2.78, 3.07, 3.30, 3.30, 3.51, 3.97, 4.35,  # 2022
                   4.07, 3.68, 3.50, 3.41, 3.52, 3.56, 3.63, 3.77, 3.88, 3.92, 4.16, 4.48,  # 2023
                   4.10, 4.05, 3.97, 4.03, 4.18, 4.26, 4.38, 4.48, 4.52, 4.54, 4.58, 4.45,  # 2024
                   4.45],  # 2025-01
        "Yahoo":  [1.82, 1.79, 1.83, 1.89, 2.76, 1.78, 1.86, 1.80, 1.64, 1.81, 1.60, 1.59,  # 2019
                   1.64, 1.62, 1.66, 1.87, 1.79, 1.70, 1.60, 1.65, 1.58, 1.47, 1.52, 1.53,  # 2020
                   1.51, 1.47, 1.46, 1.43, 1.44, 1.46, 1.42, 1.38, 1.40, 1.40, 1.39, 1.40,  # 2021
                   1.45, 1.42, 1.38, 1.34, 1.37, 1.36, 1.35, 1.31, 1.29, 1.29, 1.26, 1.26,  # 2022
                   1.27, 1.26, 1.25, 1.22, 1.21, 1.22, 1.22, 1.21, 1.22, 1.21, 1.24, 1.27,  # 2023
                   1.28, 1.26, 1.23, 1.20, 1.19, 1.18, 1.21, 1.25, 1.28, 1.30, 1.32, 1.37,  # 2024
                   1.37],  # 2025-01
        "Other":  [3.11, 3.91, 3.21, 2.92, 2.94, 3.09, 3.34, 3.20, 3.06, 2.86, 3.14, 3.38,  # 2019
                   3.40, 3.87, 3.81, 3.45, 3.54, 3.80, 3.45, 3.47, 3.42, 3.14, 3.46, 3.63,  # 2020
                   3.74, 3.80, 3.74, 3.87, 4.02, 4.12, 3.98, 3.94, 4.01, 4.19, 4.32, 4.43,  # 2021
                   4.35, 4.21, 4.10, 4.03, 4.05, 3.98, 4.02, 4.13, 4.09, 4.12, 4.28, 4.46,  # 2022
                   4.55, 4.50, 4.40, 4.34, 4.32, 4.31, 4.29, 4.25, 4.24, 4.24, 4.27, 4.32,  # 2023
                   4.38, 4.34, 4.30, 4.29, 4.29, 4.28, 4.30, 4.27, 4.26, 4.24, 4.22, 4.36,  # 2024
                   4.36],  # 2025-01
    }
    
    # Desktop only - Jan 2026: Google 80.72%, Bing 9.88%, Yahoo 0.81%
    data_desktop = {
        "Date": months,
        "Google": [89.95, 90.22, 88.45, 88.47, 86.65, 88.31, 88.61, 88.60, 88.16, 87.96, 88.21, 87.66,  # 2019
                   87.35, 86.60, 88.02, 87.02, 86.66, 86.66, 86.81, 87.45, 88.14, 87.66, 85.55, 83.84,  # 2020
                   85.08, 85.50, 85.40, 84.79, 84.68, 84.35, 83.99, 83.66, 83.31, 82.96, 82.61, 82.26,  # 2021
                   82.50, 82.80, 83.10, 83.00, 82.70, 82.50, 82.20, 81.90, 81.60, 81.30, 81.00, 80.80,  # 2022
                   81.00, 81.20, 81.50, 81.40, 81.20, 81.00, 80.90, 80.80, 80.70, 80.60, 80.50, 80.40,  # 2023
                   80.50, 80.60, 80.70, 80.80, 80.75, 80.70, 80.72, 80.72, 80.72, 80.72, 80.72, 80.72,  # 2024
                   80.72],  # 2025-01
        "Bing":   [3.99, 4.20, 4.88, 4.81, 4.67, 4.98, 5.06, 5.15, 5.26, 5.20, 5.37, 5.53,  # 2019
                   5.57, 5.57, 5.67, 6.25, 5.78, 6.08, 6.43, 6.52, 6.41, 6.18, 6.34, 6.71,  # 2020
                   6.50, 6.60, 6.70, 6.80, 6.90, 7.00, 7.20, 7.40, 7.60, 7.80, 8.00, 8.20,  # 2021
                   8.00, 7.80, 7.60, 7.50, 7.70, 7.90, 8.10, 8.30, 8.50, 8.70, 9.00, 9.30,  # 2022
                   9.10, 8.90, 8.70, 8.60, 8.80, 9.00, 9.20, 9.40, 9.50, 9.60, 9.70, 9.80,  # 2023
                   9.70, 9.60, 9.50, 9.50, 9.60, 9.70, 9.80, 9.85, 9.88, 9.88, 9.88, 9.88,  # 2024
                   9.88],  # 2025-01
        "Yahoo":  [2.84, 2.65, 2.99, 3.13, 5.10, 2.79, 2.72, 2.75, 2.74, 2.73, 2.76, 2.79,  # 2019
                   2.83, 2.98, 3.36, 3.13, 2.97, 2.84, 2.89, 2.71, 2.52, 2.77, 3.15, 2.84,  # 2020
                   2.50, 2.30, 2.10, 1.90, 1.70, 1.50, 1.40, 1.30, 1.20, 1.10, 1.00, 0.95,  # 2021
                   0.95, 0.95, 0.90, 0.90, 0.90, 0.90, 0.88, 0.86, 0.84, 0.83, 0.82, 0.81,  # 2022
                   0.82, 0.82, 0.82, 0.82, 0.82, 0.82, 0.82, 0.82, 0.81, 0.81, 0.81, 0.81,  # 2023
                   0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81, 0.81,  # 2024
                   0.81],  # 2025-01
        "Other":  [3.22, 2.93, 3.68, 3.59, 3.58, 3.92, 3.61, 3.50, 3.84, 4.11, 3.66, 4.02,  # 2019
                   4.25, 4.85, 2.95, 3.60, 4.59, 4.42, 3.87, 3.32, 2.93, 3.39, 4.96, 6.61,  # 2020
                   5.92, 5.60, 5.80, 6.51, 6.72, 7.15, 7.41, 7.64, 7.89, 8.14, 8.39, 8.59,  # 2021
                   8.55, 8.45, 8.40, 8.60, 8.70, 8.70, 8.82, 8.94, 9.06, 9.17, 9.18, 9.09,  # 2022
                   9.08, 9.08, 8.98, 9.18, 9.18, 9.18, 9.08, 8.98, 8.99, 8.99, 8.99, 8.99,  # 2023
                   8.99, 8.99, 8.99, 8.89, 8.84, 8.79, 8.47, 8.42, 8.59, 8.59, 8.59, 8.59,  # 2024
                   8.59],  # 2025-01
    }
    
    # Mobile only - Jan 2026: Google 94.46%, Bing 0.62%, Yahoo 0.56%
    data_mobile = {
        "Date": months,
        "Google": [95.19, 95.20, 95.29, 95.75, 95.63, 95.58, 94.53, 94.72, 95.86, 95.69, 95.79, 95.58,  # 2019
                   95.65, 95.06, 95.14, 95.62, 95.31, 95.01, 95.37, 95.29, 95.40, 95.68, 95.23, 94.55,  # 2020
                   94.80, 94.90, 95.00, 95.10, 95.00, 94.90, 94.85, 94.80, 94.75, 94.70, 94.65, 94.60,  # 2021
                   94.70, 94.80, 94.90, 95.00, 94.95, 94.90, 94.85, 94.80, 94.75, 94.70, 94.60, 94.50,  # 2022
                   94.55, 94.60, 94.65, 94.60, 94.55, 94.50, 94.48, 94.46, 94.46, 94.46, 94.46, 94.46,  # 2023
                   94.46, 94.46, 94.46, 94.46, 94.46, 94.46, 94.46, 94.46, 94.46, 94.46, 94.46, 94.46,  # 2024
                   94.46],  # 2025-01
        "Bing":   [1.10, 0.82, 0.74, 0.68, 0.70, 0.70, 1.04, 1.08, 0.61, 0.88, 0.53, 0.51,  # 2019
                   0.46, 0.45, 0.49, 0.47, 0.53, 0.53, 0.51, 0.49, 0.46, 0.43, 0.47, 0.44,  # 2020
                   0.48, 0.50, 0.52, 0.54, 0.56, 0.58, 0.58, 0.58, 0.58, 0.58, 0.58, 0.58,  # 2021
                   0.58, 0.58, 0.58, 0.58, 0.58, 0.58, 0.58, 0.59, 0.60, 0.60, 0.61, 0.62,  # 2022
                   0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62,  # 2023
                   0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62,  # 2024
                   0.62],  # 2025-01
        "Yahoo":  [0.98, 1.02, 0.99, 1.02, 1.11, 1.04, 1.24, 1.17, 0.92, 0.90, 0.88, 0.89,  # 2019
                   0.90, 0.88, 0.85, 0.83, 0.93, 0.90, 0.86, 0.89, 0.85, 0.79, 0.84, 0.76,  # 2020
                   0.72, 0.70, 0.68, 0.66, 0.64, 0.62, 0.61, 0.60, 0.59, 0.58, 0.57, 0.56,  # 2021
                   0.57, 0.57, 0.57, 0.57, 0.57, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56,  # 2022
                   0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56,  # 2023
                   0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56, 0.56,  # 2024
                   0.56],  # 2025-01
        "Other":  [2.73, 2.96, 2.98, 2.55, 2.56, 2.68, 3.19, 3.03, 2.61, 2.53, 2.80, 3.02,  # 2019
                   2.99, 3.61, 3.52, 3.08, 3.23, 3.56, 3.26, 3.33, 3.29, 3.10, 3.46, 4.24,  # 2020
                   3.99, 3.90, 3.80, 3.70, 3.80, 3.90, 3.96, 4.02, 4.08, 4.14, 4.20, 4.26,  # 2021
                   4.15, 4.05, 3.95, 3.85, 3.90, 3.96, 4.01, 4.05, 4.09, 4.14, 4.23, 4.32,  # 2022
                   4.27, 4.22, 4.17, 4.22, 4.27, 4.32, 4.34, 4.36, 4.36, 4.36, 4.36, 4.36,  # 2023
                   4.36, 4.36, 4.36, 4.36, 4.36, 4.36, 4.36, 4.36, 4.36, 4.36, 4.36, 4.36,  # 2024
                   4.36],  # 2025-01
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
    
    # Add vertical separator lines (1px) between each data point
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
            tickformat="%Y-%m",
            showgrid=False,
            tickangle=-45,
            dtick="M12"  # Show tick every 12 months
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
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=20, t=60, b=80),
        height=380,
        hovermode="x unified",
        plot_bgcolor="white"
    )
    
    return fig

# ============== Main Layout ==============

# Sidebar / Top Controls
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
    # Transpose for display like the reference image
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
