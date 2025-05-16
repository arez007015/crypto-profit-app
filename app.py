import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crypto DCA Profit App", layout="centered")

st.title("💰 DCA Profit/Loss Calculator")

# Load or initialize transaction history
if "trades" not in st.session_state:
    st.session_state.trades = []

st.subheader("➕ Add New Trade")
col1, col2, col3 = st.columns(3)
with col1:
    price = st.number_input("Buy Price ($)", min_value=0.0, format="%.2f")
with col2:
    amount = st.number_input("Amount (Coins)", min_value=0.0, format="%.6f")
with col3:
    date = st.date_input("Buy Date")

if st.button("Add Trade"):
    st.session_state.trades.append({"date": date, "price": price, "amount": amount})
    st.success("Trade added!")

# Show trade history
if st.session_state.trades:
    df = pd.DataFrame(st.session_state.trades)
    df["total"] = df["price"] * df["amount"]
    st.subheader("📋 Trade History")
    st.dataframe(df)

    total_amount = df["amount"].sum()
    total_cost = df["total"].sum()
    avg_price = total_cost / total_amount if total_amount != 0 else 0

    st.markdown(f"**🧮 Average Buy Price:** ${avg_price:.2f}")

    current_price = st.number_input("💵 Current Price", value=avg_price, format="%.2f")
    current_value = current_price * total_amount
    profit_loss = current_value - total_cost
    profit_percent = (profit_loss / total_cost) * 100 if total_cost != 0 else 0

    st.metric("📊 Profit/Loss ($)", f"${profit_loss:.2f}", delta=f"{profit_percent:.2f}%")

    # Plot chart
    fig, ax = plt.subplots()
    ax.axhline(avg_price, color='blue', linestyle='--', label=f'Avg Price: ${avg_price:.2f}')
    ax.axhline(current_price, color='green', linestyle='-', label=f'Current Price: ${current_price:.2f}')
    ax.set_title("Price Comparison")
    ax.set_ylabel("Price ($)")
    ax.legend()
    st.pyplot(fig)

else:
    st.info("No trades yet. Please add a trade.")
