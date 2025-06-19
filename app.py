
import streamlit as st
import pandas as pd
import plotly.express as px

# Load your CSV
df = pd.read_csv("Enriched_Marketing_Test_Examples.csv")

st.set_page_config(page_title="Marketing Test Dashboard", layout="wide")

st.title("📊 Marketing Test Dashboard")
st.write("Explore and visualize your enriched marketing test examples.")

# Sidebar filters
st.sidebar.header("Filter Options")
test_types = df['Test Type'].unique()
selected_test_types = st.sidebar.multiselect("Select Test Types:", test_types, default=test_types)

filtered_df = df[df['Test Type'].isin(selected_test_types)]

st.markdown(f"### Showing {len(filtered_df)} tests")
st.dataframe(filtered_df)

# Summary Metrics
st.subheader("📈 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,}")
col2.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,}")
avg_cr = filtered_df['Conversion Rate (%)'].mean()
col3.metric("Average Conversion Rate (%)", f"{avg_cr:.2f}%")

# Visualizations
st.subheader("🔍 Visualizations")

tab1, tab2, tab3 = st.tabs(["Conversion Rate vs Cost", "ROI Distribution", "CTR vs Impressions"])

with tab1:
    fig1 = px.scatter(filtered_df, 
                      x="Cost ($)", 
                      y="Conversion Rate (%)",
                      color="Test Type",
                      hover_data=["Example", "Recommendation"],
                      title="Conversion Rate vs Cost")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.histogram(filtered_df, 
                        x="ROI (%)",
                        color="Test Type",
                        nbins=20,
                        title="ROI (%) Distribution")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    fig3 = px.scatter(filtered_df,
                      x="Impressions",
                      y="CTR (%)",
                      color="Test Type",
                      size="Clicks",
                      hover_data=["Example"],
                      title="CTR (%) vs Impressions")
    st.plotly_chart(fig3, use_container_width=True)

# Detailed view
st.subheader("🔬 Detailed View")

selected_example = st.selectbox("Select an example to view details:", filtered_df['Example'])
example_row = filtered_df[filtered_df['Example'] == selected_example].iloc[0]

st.write(f"**Test Type:** {example_row['Test Type']}")
st.write(f"**Explanation:** {example_row['Explanation']}")
st.write(f"**Recommendation:** {example_row['Recommendation']}")
st.write(f"**Test Method:** {example_row['Test Method']}")
st.write(f"**Reason for Method:** {example_row['Reason for Method']}")

st.write("**Performance Metrics:**")
metrics = example_row[["Impressions", "Clicks", "Conversions", "Conversion Rate (%)", "Lift (%)",
                       "Cost ($)", "ROI (%)", "CTR (%)", "CPA ($)", "Revenue ($)", "Profit ($)", "Engagement Score"]]
st.json(metrics.to_dict())

st.success("✅ Dashboard ready! Customize it further as needed.")
