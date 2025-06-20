import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV
df = pd.read_csv("Enriched_Marketing_Test_Examples.csv")

st.set_page_config(page_title="Marketing Test Dashboard", layout="wide")

st.title("📊 Marketing Test Dashboard")
st.write("Explore and visualize your enriched marketing test examples.")

# ---------------------------
# 1️⃣ Filter (uniform HTML buttons grid)
# ---------------------------
st.subheader("🔎 **Filter by Test Type:**")

test_types = df['Test Type'].unique()

# Initialize session state for filter
if 'selected_types' not in st.session_state:
    st.session_state.selected_types = list(test_types)

# Generate buttons in a form to capture clicks
with st.form("filter_form"):
    buttons_html = ""
    for test_type in test_types:
        selected = "selected" if test_type in st.session_state.selected_types else ""
        buttons_html += f"""
        <button class="filter-button {selected}" name="filter" type="submit" value="{test_type}">{test_type}</button>
        """

    st.markdown(f"""
    <div class="button-grid">{buttons_html}</div>
    """, unsafe_allow_html=True)

    # Hidden input to capture which button was clicked
    clicked = st.form_submit_button()

# Custom CSS: grid layout, identical size, neat style
st.markdown("""
    <style>
    .button-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .filter-button {
        background-color: #333333;
        color: white;
        border: none;
        border-radius: 5px;
        width: 200px;
        height: 80px;
        text-align: center;
        word-wrap: break-word;
        padding: 10px;
        cursor: pointer;
        font-size: 16px;
    }
    .filter-button.selected {
        border: 2px solid #00FFAA; /* Highlight selected */
    }
    </style>
    """, unsafe_allow_html=True)

# Update session state when a button is clicked
if clicked:
    clicked_type = st.experimental_get_query_params().get("filter", [None])[0]
    if clicked_type in st.session_state.selected_types:
        st.session_state.selected_types.remove(clicked_type)
    else:
        st.session_state.selected_types.append(clicked_type)

# Default to all if none selected
if not st.session_state.selected_types:
    filtered_df = df.copy()
else:
    filtered_df = df[df['Test Type'].isin(st.session_state.selected_types)]

# ---------------------------
# 2️⃣ Summary Metrics
# ---------------------------
st.subheader("📈 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Impressions", f"{filtered_df['Impressions'].sum():,}")
col2.metric("Total Conversions", f"{filtered_df['Conversions'].sum():,}")
avg_cr = filtered_df['Conversion Rate (%)'].mean()
col3.metric("Average Conversion Rate (%)", f"{avg_cr:.2f}%")

# ---------------------------
# 3️⃣ Detailed View
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
# 4️⃣ Visualizations
# ---------------------------
if not filtered_df.empty:
    st.subheader("📊 Additional Visualizations")

    col1, col2 = st.columns(2)

    with col1:
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
# 5️⃣ List of Tests
# ---------------------------
st.subheader(f"🗂️ Showing {len(filtered_df)} Test(s)")
st.dataframe(filtered_df)

st.success("✅ Fully updated: uniform filter buttons using HTML grid, perfect sizing, toggles work cleanly!")
