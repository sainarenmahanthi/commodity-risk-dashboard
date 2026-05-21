import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Setup
# --------------------------------------------------
st.set_page_config(
    page_title="SME Commodity Risk Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = pd.read_csv("integrated_commodity_dataset.csv")

df["Date"] = pd.to_datetime(
    df["Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

df = df.dropna(subset=["Date"])
df = df.sort_values("Date")

commodities = ["Gold_USD", "Silver_USD", "Crude_Oil"]

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("Dashboard Navigation")

st.sidebar.write("""
This dashboard helps SMEs monitor:

- Commodity price trends
- Shock periods
- Rolling volatility
- Risk levels
- Forecast insights
""")

commodity = st.sidebar.selectbox(
    "Select Commodity",
    commodities
)

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("SME Commodity Risk Dashboard")

st.write(
    "This dashboard helps small and medium-sized businesses understand "
    "commodity price trends, volatility, shock periods, and possible risk levels."
)

# --------------------------------------------------
# Risk Logic
# --------------------------------------------------
latest_price = df[commodity].dropna().iloc[-1]
recent_return = df[commodity].pct_change().dropna().iloc[-1]

if commodity == "Gold_USD":
    risk = "Low Risk"
    explanation = "Gold shows stable long-term growth and lower volatility."
elif commodity == "Silver_USD":
    risk = "Moderate Risk"
    explanation = "Silver shows moderate volatility and reacts to both investment and industrial demand."
else:
    risk = "High Risk"
    explanation = "Crude oil is highly volatile and sensitive to global events, fuel demand, and supply shocks."

# --------------------------------------------------
# Metrics
# --------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Latest Price", round(latest_price, 2))
col2.metric("Recent Return", f"{recent_return * 100:.2f}%")

with col3:
    st.write("Risk Level")
    if risk == "Low Risk":
        st.success(risk)
    elif risk == "Moderate Risk":
        st.warning(risk)
    else:
        st.error(risk)

# --------------------------------------------------
# Simple Explanation
# --------------------------------------------------
st.subheader("Simple SME Explanation")
st.write(explanation)

# --------------------------------------------------
# Price Trend Chart
# --------------------------------------------------
st.subheader("Price Trend")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df["Date"], df[commodity], label=commodity)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.set_title(f"{commodity} Price Trend")
ax.legend()

st.pyplot(fig)

# --------------------------------------------------
# Shock Detection
# --------------------------------------------------
st.subheader("Shock Detection")

df[f"{commodity}_Return"] = df[commodity].pct_change()
threshold = df[f"{commodity}_Return"].std() * 3
df["Shock"] = abs(df[f"{commodity}_Return"]) > threshold

shock_points = df[df["Shock"] == True]

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(df["Date"], df[commodity], label="Price")
ax2.scatter(
    shock_points["Date"],
    shock_points[commodity],
    marker="x",
    label="Shock Point"
)

ax2.set_xlabel("Date")
ax2.set_ylabel("Price")
ax2.set_title(f"{commodity} Shock Detection")
ax2.legend()

st.pyplot(fig2)

st.write(
    f"Detected shock points for {commodity}: **{len(shock_points)}**"
)

# --------------------------------------------------
# Rolling Volatility
# --------------------------------------------------
st.subheader("Rolling Volatility")

df[f"{commodity}_Volatility"] = df[f"{commodity}_Return"].rolling(6).std()

fig3, ax3 = plt.subplots(figsize=(12, 5))
ax3.plot(df["Date"], df[f"{commodity}_Volatility"])
ax3.set_xlabel("Date")
ax3.set_ylabel("Rolling Volatility")
ax3.set_title(f"{commodity} Rolling Volatility")

st.pyplot(fig3)

# --------------------------------------------------
# Business Recommendation
# --------------------------------------------------
st.subheader("Business Recommendation")

if commodity == "Gold_USD":
    st.write(
        "Jewelers and businesses dealing with gold can use this dashboard "
        "to monitor long-term price growth and plan inventory purchases during stable periods."
    )

elif commodity == "Silver_USD":
    st.write(
        "Businesses using silver should monitor volatility because silver can react "
        "to both market uncertainty and industrial demand changes."
    )

else:
    st.write(
        "Restaurants, logistics firms, delivery businesses, and transport-dependent SMEs "
        "should monitor crude oil closely because sudden oil shocks can increase fuel "
        "and operating costs."
    )

# --------------------------------------------------
# Forecast Insight
# --------------------------------------------------
st.subheader("Forecast Insight")

st.write(
    "Baseline ARIMA forecasting suggests relatively stable short-term movement. "
    "However, crude oil remains higher risk because historical shock periods show "
    "strong sensitivity to global disruptions."
)

# --------------------------------------------------
# Final Summary
# --------------------------------------------------
st.subheader("Overall Risk Summary")

risk_summary = pd.DataFrame({
    "Commodity": ["Gold", "Silver", "Crude Oil"],
    "Risk Level": ["Low", "Moderate", "High"],
    "Main Reason": [
        "Stable long-term growth and lower volatility",
        "Moderate volatility and industrial demand sensitivity",
        "High volatility and sensitivity to global shocks"
    ]
})

st.table(risk_summary)