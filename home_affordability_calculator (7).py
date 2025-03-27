
import streamlit as st

# ------------------ Data ------------------
loan_formulas = {
    "C.3.0 – 3% down closing costs out of pocket": {"down_payment": 3, "seller_concession": 0, "max_ltv": 97},
    "C.3.3 – 3% down 3% seller credit": {"down_payment": 3, "seller_concession": 3, "max_ltv": 97},
    "C.5.0 – 5% down 0% seller credit": {"down_payment": 5, "seller_concession": 0, "max_ltv": 95},
    "C.5.3 – 5% down 3% seller credit": {"down_payment": 5, "seller_concession": 3, "max_ltv": 95},
    "C.10.0 – 10% down 0% seller credit": {"down_payment": 10, "seller_concession": 0, "max_ltv": 90},
    "C.10.6 – Optimized 10% down 6% seller credit": {"down_payment": 10, "seller_concession": 6, "max_ltv": 90},
    "C.15.0 – 15% down 0% seller credit": {"down_payment": 15, "seller_concession": 0, "max_ltv": 85},
    "C.15.2 – 15% down 2% seller credit": {"down_payment": 15, "seller_concession": 2, "max_ltv": 85},
    "C.15.6 – 15% down 6% seller credit": {"down_payment": 15, "seller_concession": 6, "max_ltv": 85},
    "C.20.0 – 20% down 0% seller credit": {"down_payment": 20, "seller_concession": 0, "max_ltv": 80},
    "C.20.2 – 20% down 2% seller credit": {"down_payment": 20, "seller_concession": 2, "max_ltv": 80},
    "C.20.6 – 20% down 6% seller credit": {"down_payment": 20, "seller_concession": 6, "max_ltv": 80},
    "C.25.0 – 25% down 0% seller credit": {"down_payment": 25, "seller_concession": 0, "max_ltv": 75},
    "C.25.2 – 25% down 2% seller credit": {"down_payment": 25, "seller_concession": 2, "max_ltv": 75},
    "C.25.6 – 25% down 6% seller credit": {"down_payment": 25, "seller_concession": 6, "max_ltv": 75},
    "HB.10.0 – High-balance 10% 0% seller credit": {"down_payment": 10, "seller_concession": 0, "max_ltv": 90},
    "HB.10.6 – High-balance 10% 6% seller credit": {"down_payment": 10, "seller_concession": 6, "max_ltv": 90},
    "HB.15.0 – High-balance 15% 0% seller credit": {"down_payment": 15, "seller_concession": 0, "max_ltv": 85},
    "HB.15.6 – High-balance 15% 6% seller credit": {"down_payment": 15, "seller_concession": 6, "max_ltv": 85},
    "HB.20.0 – High-balance 20% 0% seller credit": {"down_payment": 20, "seller_concession": 0, "max_ltv": 80},
    "HB.20.6 – High-balance 20% 6% seller credit": {"down_payment": 20, "seller_concession": 6, "max_ltv": 80},
    "HB.25.0 – High-balance 25% 0% seller credit": {"down_payment": 25, "seller_concession": 0, "max_ltv": 75},
    "HB.25.6 – High-balance 25% 6% seller credit": {"down_payment": 25, "seller_concession": 6, "max_ltv": 75},
    "HB.25.9 – High-balance 25% 9% seller credit": {"down_payment": 25, "seller_concession": 9, "max_ltv": 75}
}

loan_limits = {
    1: {"conforming": 806500, "high_balance": 1209750},
    2: {"conforming": 1032650, "high_balance": 1548975},
    3: {"conforming": 1248150, "high_balance": 1872225},
    4: {"conforming": 1551250, "high_balance": 2326875}
}

# ------------------ Loan Calculation ------------------
def calculate_loan(purchase_price, loan_term, interest_rate, down_payment_pct, seller_concession_pct, property_tax, home_insurance, flood_insurance):
    try:
        total_sale_price = purchase_price / (1 - seller_concession_pct)
        loan_amount = total_sale_price * (1 - down_payment_pct)
        cash_to_close = total_sale_price * down_payment_pct

        monthly_interest_rate = (interest_rate / 100) / 12
        num_payments = loan_term * 12
        monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -num_payments)

        monthly_property_tax = property_tax / 12
        monthly_home_insurance = home_insurance / 12
        monthly_flood_insurance = flood_insurance / 12

        total_monthly_payment = monthly_payment + monthly_property_tax + monthly_home_insurance + monthly_flood_insurance

        return total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment
    except ZeroDivisionError:
        st.error("Seller concession percentage cannot be 100%. Please enter a valid percentage.")
        return None, None, None, None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None, None, None, None

# ------------------ UI ------------------
st.title("🏡 Home Affordability Calculator")

col1, col2, col3 = st.columns(3)

with col1:
    occupancy_type = st.selectbox("🏡 Occupancy", ["Primary Residence", "Second Home", "Investment Property"])
    num_units = st.selectbox("🏢 Units", [1, 2, 3, 4])
    purchase_price = float(st.number_input("💰 Price ($)", min_value=50000.0, value=807000.0, step=5000.0))

with col2:
    loan_term = float(st.number_input("🗓 Term (Years)", min_value=5.0, max_value=30.0, step=5.0, value=30.0))
    interest_rate = float(st.number_input("📊 Interest (%)", min_value=1.0, max_value=10.0, step=0.001, value=5.625))

with col3:
    property_tax = float(st.number_input("🏡 Tax ($)", min_value=0.0, value=0.0, step=100.0))
    home_insurance = float(st.number_input("🔒 Insurance ($)", min_value=0.0, value=0.0, step=100.0))
    flood_insurance = float(st.number_input("🌊 Flood Ins. ($)", min_value=0.0, value=0.0, step=100.0))

selected_formula = st.selectbox("📜 Loan Formula", list(loan_formulas.keys()))

if st.button("📊 Calculate Loan & Monthly Payment"):
    formula = loan_formulas[selected_formula]
    down_payment_pct = formula["down_payment"] / 100
    seller_concession_pct = formula["seller_concession"] / 100

    total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
        purchase_price, loan_term, interest_rate, down_payment_pct, seller_concession_pct,
        property_tax, home_insurance, flood_insurance
    )

    if total_sale_price is None:
        st.stop()

    show_original_results = True
    errors = []

    limits = loan_limits[num_units]
    if selected_formula.startswith("C") and loan_amount > limits["conforming"]:
        show_original_results = False
        errors.append(f"Loan exceeds conforming limit for {num_units}-unit: ${limits['conforming']:,.2f}")

    elif selected_formula.startswith("HB") and (loan_amount <= limits["conforming"] or loan_amount > limits["high_balance"]):
        show_original_results = False
        errors.append(f"Loan must be between conforming (${limits['conforming']:,.2f}) and high-balance (${limits['high_balance']:,.2f})")

    if loan_amount > limits["high_balance"]:
        show_original_results = False
        errors.append(f"Loan exceeds high-balance max for {num_units}-unit: ${limits['high_balance']:,.2f}")

    if not show_original_results:
        for msg in errors:
            st.markdown(f'<div style="background-color:red; color:white; padding:10px;">{msg}</div>', unsafe_allow_html=True)

        # Suggest higher down payment
        if total_sale_price > 0:
            adjusted_down_payment_pct = ((loan_amount - limits["conforming"]) / total_sale_price) + down_payment_pct
            if adjusted_down_payment_pct < 1.0:
                new_cash_to_close = total_sale_price * adjusted_down_payment_pct
                if st.button(f"✅ Apply {adjusted_down_payment_pct:.2%} Down Payment & Recalculate\nTotal Cash to Close: ${new_cash_to_close:,.2f}"):
                    total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
                        purchase_price, loan_term, interest_rate, adjusted_down_payment_pct, seller_concession_pct,
                        property_tax, home_insurance, flood_insurance
                    )
                    st.subheader("💼 Adjusted Loan Summary")
                    st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
                    st.write(f"Loan Amount: ${loan_amount:,.2f}")
                    st.write(f"Cash to Close: ${cash_to_close:,.2f}")
                    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
                    st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

        # Suggest alternative formula
        for alt_formula, values in loan_formulas.items():
            if alt_formula != selected_formula:
                alt_down = values["down_payment"] / 100
                alt_loan_amt = (purchase_price / (1 - values["seller_concession"] / 100)) * (1 - alt_down)
                if alt_formula.startswith("C") and alt_loan_amt <= limits["conforming"]:
                    new_cash = purchase_price * alt_down / (1 - values["seller_concession"] / 100)
                    if st.button(f"🔄 Switch to {alt_formula}\nTotal Cash to Close: ${new_cash:,.2f}"):
                        selected_formula = alt_formula
                        st.experimental_rerun()
                    break
    else:
        st.subheader("💼 Loan Summary")
        st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
        st.write(f"Loan Amount: ${loan_amount:,.2f}")
        st.write(f"Cash to Close: ${cash_to_close:,.2f}")
        st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
        st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

