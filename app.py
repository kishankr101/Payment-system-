import streamlit as st
import time
import random

st.set_page_config(page_title="International Payment Simulator", layout="wide")

# -------------------------------
# Title
# -------------------------------
st.title("🌍 International Payment Processing Simulator")
st.markdown("Simulates how global payments work (KYC → Bank → Network → Forex → Settlement)")

# -------------------------------
# Sidebar - User Input
# -------------------------------
st.sidebar.header("👤 User Details")

name = st.sidebar.text_input("Full Name")
pan = st.sidebar.text_input("PAN Number")
amount = st.sidebar.number_input("Amount (INR)", min_value=1.0)
currency = st.sidebar.selectbox("Convert To", ["USD", "EUR", "GBP"])
network = st.sidebar.selectbox("Payment Network", ["Visa", "Mastercard", "SWIFT"])

# -------------------------------
# Exchange Rates (Mock)
# -------------------------------
rates = {
    "USD": 83,
    "EUR": 90,
    "GBP": 105
}

# -------------------------------
# KYC Check
# -------------------------------
def kyc_verification(name, pan):
    if len(name) > 3 and len(pan) == 10:
        return True
    return False

# -------------------------------
# Fee Calculation
# -------------------------------
def calculate_fees(amount):
    app_fee = amount * 0.01
    bank_fee = amount * 0.015
    forex_fee = amount * 0.02
    return app_fee, bank_fee, forex_fee

# -------------------------------
# Transaction Flow
# -------------------------------
def process_payment():
    steps = [
        "🔐 KYC Verification",
        "🏦 Bank Processing",
        "🌐 Payment Network Routing",
        "💱 Currency Conversion",
        "🌍 International Settlement",
        "✅ Payment Completed"
    ]

    progress = st.progress(0)

    for i, step in enumerate(steps):
        st.info(step)
        time.sleep(1.2)
        progress.progress((i + 1) / len(steps))

# -------------------------------
# Main Button
# -------------------------------
if st.button("🚀 Process Payment"):

    if not kyc_verification(name, pan):
        st.error("❌ KYC Failed! Enter valid details.")
    else:
        st.success("✅ KYC Verified")

        # Fees
        app_fee, bank_fee, forex_fee = calculate_fees(amount)
        total_fee = app_fee + bank_fee + forex_fee

        # Conversion
        converted_amount = (amount - total_fee) / rates[currency]

        # Process Simulation
        process_payment()

        # -------------------------------
        # Result Section
        # -------------------------------
        st.subheader("💰 Transaction Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Original Amount (INR)", f"₹{amount}")
            st.metric("Total Fees", f"₹{round(total_fee,2)}")

        with col2:
            st.metric(f"Converted ({currency})", f"{round(converted_amount,2)} {currency}")
            st.metric("Network Used", network)

        # -------------------------------
        # Fee Breakdown
        # -------------------------------
        st.subheader("📊 Fee Breakdown")
        st.write(f"App Fee: ₹{round(app_fee,2)}")
        st.write(f"Bank Fee: ₹{round(bank_fee,2)}")
        st.write(f"Forex Fee: ₹{round(forex_fee,2)}")

        # -------------------------------
        # Transaction ID
        # -------------------------------
        txn_id = "TXN" + str(random.randint(100000, 999999))
        st.success(f"🎉 Transaction Successful! ID: {txn_id}")

        # -------------------------------
        # History (Session)
        # -------------------------------
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({
            "id": txn_id,
            "amount": amount,
            "currency": currency,
            "converted": round(converted_amount,2)
        })

# -------------------------------
# Transaction History
# -------------------------------
st.subheader("📜 Transaction History")

if "history" in st.session_state:
    for txn in st.session_state.history[::-1]:
        st.write(f"ID: {txn['id']} | ₹{txn['amount']} → {txn['converted']} {txn['currency']}")
else:
    st.write("No transactions yet.")
