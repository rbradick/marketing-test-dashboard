import streamlit as st
import pandas as pd
import plotly.express as px
from functools import lru_cache

# ---------------------------
# Configuration and Data Loading
# ---------------------------
st.set_page_config(page_title="Marketing Test Dashboard", layout="wide")
st.title("📊 Marketing Test Dashboard")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Enriched_Marketing_Test_Examples.csv")
        # Ensure numeric columns are properly formatted
        numeric_cols = ['Impressions', 'Clicks', 'Conversions', 'Conversion Rate (%)',
                       'Lift (%)', 'Cost ($)', 'ROI (%)', 'CTR (%)', 'CPA ($)',
                       'Revenue ($)', 'Profit ($)', 'Engagement Score']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available. Please check your data file.")
    st.stop()

# ---------------------------
# Sidebar Filters
# ---------------------------
st.sidebar.header("🔍 Filters")

# Test Type filter
test_types = df['Test Type'].unique().tolist()
selected_test_types = st.sidebar.multiselect(
    "Select Test Types:",
    options=test_types,
    default=test_types[:1],  # Default to first option
    help="Select one or more test types to analyze"
)

# Date range filter (if date column exists)
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if len(date_range) == 2:
        filtered_df = df[
            (df['Test Type'].isin(selected_test_types)) &
            (df['Date'].dt.date >= date_range[0]) &
            (df['Date'].dt.date <= date_range[1])
        ]
    else:
        filtered_df = df[df['Test Type'].isin(selected_test_types)]
else:
    filtered_df = df[df['Test Type'].isin(selected_test_types)] if selected_test_types else df.iloc[0:0]

# ---------------------------
# Main Dashboard
# ---------------------------
if not filtered_df.empty:
    st.write(f"### 📋 Showing {len(filtered_df)} tests")
    
    # Summary Metrics
    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,}")
    col2.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,}")
    avg_cr = filtered_df['Conversion Rate (%)'].mean()
    col3.metric("Avg Conversion Rate", f"{avg_cr:.2f}%")
    col4.metric("Total Revenue", f"${filtered_df['Revenue ($)'].sum():,.2f}")
    
    # Visualizations
    st.subheader("📊 Performance Visualizations")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Conversion Analysis", 
        "💰 ROI & Cost", 
        "👆 CTR & Engagement",
        "📅 Trends Over Time"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig1a = px.scatter(
                filtered_df, 
                x="Cost ($)", 
                y="Conversion Rate (%)",
                color="Test Type",
                hover_data=["Example", "Recommendation"],
                title="Conversion Rate vs Cost"
            )
            st.plotly_chart(fig1a, use_container_width=True)
        with col2:
            fig1b = px.box(
                filtered_df,
                x="Test Type",
                y="Conversion Rate (%)",
                title="Conversion Rate Distribution by Test Type"
            )
            st.plotly_chart(fig1b, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig2a = px.histogram(
                filtered_df, 
                x="ROI (%)",
                color="Test Type",
                nbins=20,
                title="ROI (%) Distribution"
            )
            st.plotly_chart(fig2a, use_container_width=True)
        with col2:
            fig2b = px.scatter(
                filtered_df,
                x="Cost ($)",
                y="ROI (%)",
                color="Test Type",
                size="Revenue ($)",
                title="ROI vs Cost"
            )
            st.plotly_chart(fig2b, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            fig3a = px.scatter(
                filtered_df,
                x="Impressions",
                y="CTR (%)",
                color="Test Type",
                size="Clicks",
                hover_data=["Example"],
                title="CTR (%) vs Impressions"
            )
            st.plotly_chart(fig3a, use_container_width=True)
        with col2:
            fig3b = px.bar(
                filtered_df.groupby('Test Type')['Engagement Score'].mean().reset_index(),
                x="Test Type",
                y="Engagement Score",
                title="Average Engagement by Test Type"
            )
            st.plotly_chart(fig3b, use_container_width=True)
    
    with tab4:
        if 'Date' in filtered_df.columns:
            fig4 = px.line(
                filtered_df.groupby(['Date', 'Test Type']).agg({
                    'Conversions': 'sum',
                    'Impressions': 'sum',
                    'CTR (%)': 'mean'
                }).reset_index(),
                x="Date",
                y="Conversions",
                color="Test Type",
                title="Conversion Trends Over Time",
                facet_col="Test Type",
                facet_col_wrap=2
            )
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Date column not available for trend analysis")
    
    # Detailed View
    st.subheader("🔬 Test Details")
    selected_example = st.selectbox(
        "Select an example to view details:",
        filtered_df['Example'].unique()
    )
    
    example_row = filtered_df[filtered_df['Example'] == selected_example].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Test Information**")
        st.write(f"- **Test Type:** {example_row['Test Type']}")
        st.write(f"- **Test Method:** {example_row['Test Method']}")
        st.write(f"- **Reason for Method:** {example_row['Reason for Method']}")
        st.write(f"- **Explanation:** {example_row['Explanation']}")
        st.write(f"- **Recommendation:** {example_row['Recommendation']}")
    
    with col2:
        st.write("**Performance Metrics**")
        metrics = example_row[[
            "Impressions", "Clicks", "Conversions", "Conversion Rate (%)",
            "Lift (%)", "Cost ($)", "ROI (%)", "CTR (%)",
            "CPA ($)", "Revenue ($)", "Profit ($)", "Engagement Score"
        ]]
        st.dataframe(metrics.to_frame().style.format("{:,.2f}"))
    
else:
    st.warning("No data matches your filters. Please adjust your selection.")
