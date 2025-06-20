import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("Enriched_Marketing_Test_Examples.csv")

st.set_page_config(page_title="Marketing Test Dashboard", layout="wide")

st.title("📊 Marketing Test Dashboard")
st.write("Explore and visualize your enriched marketing test examples.")

# ---------------------------
# 1️⃣ Filter (prominent multi-select)
# ---------------------------
test_types = df['Test Type'].unique()
selected_test_types = st.multiselect(
    "🔎 **Filter by Test Type:**",
    options=test_types,
    default=list(test_types)
)

filtered_df = df[df['Test Type'].isin(selected_test_types)]

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
# 4️⃣ List of Tests (after Detailed View)
# ---------------------------
st.subheader(f"🗂️ Showing {len(filtered_df)} Test(s)")
st.dataframe(filtered_df)

# ---------------------------
# 5️⃣ Re-add Visualizations (below table)
# ---------------------------
if not filtered_df.empty:
    st.subheader("📊 Additional Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        fig_roi = px.histogram(
            filtered_df,
            x="ROI (%)",
            color="Test Type",
            nbins=20,
            title="ROI (%) Distribution"
        )
        st.plotly_chart(fig_roi, use_container_width=True)

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

st.success("✅ Dashboard fully updated with multi-select filter and charts!")
