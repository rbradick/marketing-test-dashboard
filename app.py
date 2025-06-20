import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("Enriched_Marketing_Test_Examples.csv")

st.set_page_config(page_title="Marketing Test Dashboard", layout="wide")

st.title("📊 Marketing Test Dashboard")
st.write("Explore and visualize your enriched marketing test examples.")

# ---------------------------
# 1️⃣ Filter (buttons, same size)
# ---------------------------
st.subheader("🔎 **Filter by Test Type:**")

test_types = df['Test Type'].unique()

# Initialize session state for filter
if 'selected_types' not in st.session_state:
    st.session_state.selected_types = list(test_types)

# Filter buttons
filter_cols = st.columns(len(test_types))

for i, test_type in enumerate(test_types):
    if test_type in st.session_state.selected_types:
        if filter_cols[i].button(f"✅ {test_type}", key=f"{test_type}_on"):
            st.session_state.selected_types.remove(test_type)
    else:
        if filter_cols[i].button(f"{test_type}", key=f"{test_type}_off"):
            st.session_state.selected_types.append(test_type)

# Default to all if none selected
if not st.session_state.selected_types:
    filtered_df = df.copy()
else:
    filtered_df = df[df['Test Type'].isin(st.session_state.selected_types)]

# ✅ Custom CSS: same size buttons + style
st.markdown("""
    <style>
    div[data-testid="column"] > div > button {
        background-color: #333333;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.8em 1em;
        width: 200px;               /* Fixed width */
        height: 60px;               /* Fixed height */
        white-space: normal;        /* Allow wrap */
        word-break: break-word;     /* Wrap long words */
        text-align: center;         /* Center text */
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# 2️⃣ Summary Metrics (top)
# ---------------------------
st.subheader("📈 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,}")
col2.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,}")
avg_cr = filtered_df['Conversion Rate (%)'].mean()
col3.metric("Average Conversion Rate (%)", f"{avg_cr:.2f}%")

# ---------------------------
# 3️⃣ Detailed View (next)
# ---------------------------
st.subheader("🔬 Detailed View")

if not filtered_df.empty:
    selected_example = st.selectbox(
        "Select an example to view details:",
        filtered_df['Example']
    )

    example_row = filtered_df[filtered_df['Example'] == selected_example].iloc[0]

    st.write(f"**Test Type:** {example_row['Test Type']}")
    st.write(f"**Explanation:** {example_row['Explanation']}")
    st.write(f"**Recommendation:** {example_row['Recommendation']}")
    st.write(f"**Test Method:** {example_row['Test Method']}")
    st.write(f"**Reason for Method:** {example_row['Reason for Method']}")

    st.write("**Performance Metrics:**")
    metrics = example_row[[
        "Impressions", "Clicks", "Conversions", "Conversion Rate (%)",
        "Lift (%)", "Cost ($)", "ROI (%)", "CTR (%)",
        "CPA ($)", "Revenue ($)", "Profit ($)", "Engagement Score"
    ]]
    st.json(metrics.to_dict())
else:
    st.warning("No examples found for the selected filter.")

# ---------------------------
# 4️⃣ Visualizations (next)
# ---------------------------
if not filtered_df.empty:
    st.subheader("📊 Additional Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        # ROI vs Spend Bubble Chart
        fig_roi_spend = px.scatter(
            filtered_df,
            x="Cost ($)",
            y="ROI (%)",
            size="Impressions",
            color="Test Type",
            hover_data=["Example"],
            title="ROI (%) vs Cost ($) Bubble Chart"
        )
        st.plotly_chart(fig_roi_spend, use_container_width=True)

    with col2:
        fig_ctr = px.scatter(
            filtered_df,
            x="Impressions",
            y="CTR (%)",
            color="Test Type",
            size="Clicks",
            hover_data=["Example"],
            title="CTR (%) vs Impressions"
        )
        st.plotly_chart(fig_ctr, use_container_width=True)

# ---------------------------
# 5️⃣ List of Tests (bottom)
# ---------------------------
st.subheader(f"🗂️ Showing {len(filtered_df)} Test(s)")
st.dataframe(filtered_df)

st.success("✅ Dashboard fully updated: filter buttons same size, charts reordered, and new bubble chart in place!")
