import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
@st.cache_data
def load_data():
    file_path = "D:/21 Week/EDA( Nifty 50)/NIFTY50_all.csv"  
    df = pd.read_csv(file_path)

    #
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort values for consistency
    df = df.sort_values(by=["Symbol", "Date"])

    return df

df = load_data()


st.sidebar.title("📊 NIFTY 50 Stock Analysis")
selected_stock = st.sidebar.selectbox("Select a Stock", df["Symbol"].unique())
selected_metric = st.sidebar.selectbox("Select Metric", ["Close", "Volume", "Turnover", "%Deliverable"])


stock_df = df[df["Symbol"] == selected_stock]


st.title(f"📈 NIFTY 50 Stock Dashboard - {selected_stock}")


st.subheader("📌 Stock Price Trends")
fig1 = px.line(stock_df, x="Date", y="Close", title=f"{selected_stock} Closing Price Over Time")
st.plotly_chart(fig1)


stock_df["50_MA"] = stock_df["Close"].rolling(50).mean()
stock_df["200_MA"] = stock_df["Close"].rolling(200).mean()

st.subheader("📌 Moving Averages (50 & 200 Days)")
fig2 = px.line(stock_df, x="Date", y=["Close", "50_MA", "200_MA"], labels={"value": "Price"}, title="Moving Averages")
st.plotly_chart(fig2)


st.subheader("📌 Rolling Volatility (21-Day)")
stock_df["Volatility"] = stock_df["Close"].pct_change().rolling(21).std()
fig3 = px.line(stock_df, x="Date", y="Volatility", title="Stock Volatility Over Time")
st.plotly_chart(fig3)


st.subheader(f"📌 {selected_metric} Trends")
fig4 = px.line(stock_df, x="Date", y=selected_metric, title=f"{selected_stock} {selected_metric} Over Time")
st.plotly_chart(fig4)


st.subheader("📌 Deliverable Volume & % Deliverable")
fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=stock_df["Date"], y=stock_df["Deliverable Volume"], mode='lines', name='Deliverable Volume'))
fig5.add_trace(go.Scatter(x=stock_df["Date"], y=stock_df["%Deliverble"], mode='lines', name='% Deliverable'))
fig5.update_layout(title="Deliverable Volume & % Deliverable Over Time", xaxis_title="Date")
st.plotly_chart(fig5)


st.subheader("📌 Sector-Wise Performance (Simulated)")
sector_data = pd.DataFrame({
    "Sector": ["IT", "Banking", "Pharma", "Energy", "Auto", "FMCG"],
    "Average Return (%)": [12, 8, 10, 5, 7, 9]
})
fig6 = px.bar(sector_data, x="Sector", y="Average Return (%)", title="Sector-wise Returns")
st.plotly_chart(fig6)

st.sidebar.markdown("🚀 Built by Soham")
