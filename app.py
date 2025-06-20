import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("Enriched_Marketing_Test_Examples.csv")

st.set_page_config(page_title="Marketing Test Dashboard", layout="wide")

st.title("📊 Marketing Test Dashboard")
st.write("Explore and visualize your enriched marketing test examples.")

# ---------------------------
# 1️⃣ Filter (classic buttons, red)
# ---------------------------
st.subheader("🔎 **Filter by Test Type:**")

test_types = df['Test Type'].unique()

# Initialize session state
if 'selected_types' not in st.session_state:
    st.session_state.selected_types = list(test_types)

# Create columns for buttons
filter_cols = st.columns(len(test_types))

for i, test_type in enumerate(test_types):
    if test_type in st.session_state.selected_types:
        if filter_cols[i].button(f"✅ {test_type}", key=f"{test_type}_on"):
            st.session_state.selected_types.remove(test_type)
    else:
        if filter_cols[i].button(f"{test_type}", key=f"{test_type}_off"):
            st.session_state.selected_types.append(test_type)

# ✅ Custom CSS for red buttons + same size
st.markdown("""
    <style>
    div[data-testid="column"] > div > button {
        background-color: #d32f2f; /* red */
        color: white;
        border: none;
        border-radius: 4px;
        width: 200px;       /* Fixed width */
        height: 80px;       /* Fixed height */
        display: flex;      /* Flex to center text */
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 10px;
        white-space: normal;
        word-break: break-word;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# 2️⃣ Filtered DataFrame
# ---------------------------
if not st.session_state.selected_types:
    filtered_df = df.copy()
else:
    filtered_df = df[df['Test Type'].isin(st.session_state.selected_types)]

# ---------------------------
# 3️⃣ Summary Metrics
# ---------------------------
st.subheader("📈 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,}")
col2.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,}")
avg_cr = filtered_df['Conversion Rate (%)'].mean()
col3.metric("Average Conversion Rate (%)", f"{avg_cr:.2f}%")

# ---------------------------
# 4️⃣ Detailed View
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
# 5️⃣ Visualizations
# ---------------------------
if not filtered_df.empty:
    st.subheader("📊 Additional Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        fig_roi_spend = px.scatter(
            filtered_df,
            x="Cost ($)",
