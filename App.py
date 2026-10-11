
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Candle Psychology Board", layout="wide")

st.title("📊 Candle Psychology Board")
st.write("Upload CSV candle data to analyze market prices.")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.lower()

    st.dataframe(df, use_container_width=True)

    required = ["open", "high", "low", "close"]

    if all(c in df.columns for c in required):
        for c in required:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        df = df.dropna(subset=required)

        fig = go.Figure(data=[go.Candlestick(
            x=df["time"] if "time" in df.columns else df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"]
        )])

        fig.update_layout(
            title="Candlestick Chart",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

        if not df.empty:
            st.metric("Latest Close", f"{df['close'].iloc[-1]:.5f}")
    else:
        st.error("CSV must contain open, high, low, close columns.")

st.caption("Educational analysis only. No guaranteed trading signals.")
