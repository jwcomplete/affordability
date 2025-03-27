
if total_sale_price and loan_amount and cash_to_close and monthly_payment and total_monthly_payment:
    st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
    st.write(f"Loan Amount: ${loan_amount:,.2f}")
    st.write(f"Cash to Close: ${cash_to_close:,.2f}")
    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
    st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

    # Validate conforming formulas
    if selected_formula.startswith("C") and loan_amount > loan_limits[num_units]["conforming"]:
        st.markdown(f'<div style="background-color:red; color:white; padding:10px; font-size:16px;">'
                    f'<strong>Loan amount (${loan_amount:,.2f}) exceeds the conforming limit for {num_units}-unit property (${loan_limits[num_units]["conforming"]:,.2f}).</strong></div>',
                    unsafe_allow_html=True)

        # Hide original results
        st.write("")
        st.write("")

        # Option to apply new down payment and recalculate
        adjusted_down_payment_pct = ((loan_amount - loan_limits[num_units]["conforming"]) / total_sale_price) + down_payment_pct
        new_cash_to_close = total_sale_price * adjusted_down_payment_pct

        st.session_state.adjusted_down_payment = adjusted_down_payment_pct
        st.session_state.new_cash_to_close = new_cash_to_close

        if st.button(f"✅ Apply {adjusted_down_payment_pct:.2f}% Down Payment & Recalculate\nTotal Cash to Close: ${new_cash_to_close:,.2f}"):
            st.write("")  # Clear original results
            down_payment_pct = adjusted_down_payment_pct
            total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
                purchase_price, loan_term, interest_rate, down_payment_pct, seller_concession_pct, property_tax, home_insurance, flood_insurance
            )

            if total_sale_price and loan_amount and cash_to_close and monthly_payment and total_monthly_payment:
                st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
                st.write(f"Loan Amount: ${loan_amount:,.2f}")
                st.write(f"Cash to Close: ${cash_to_close:,.2f}")
                st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
                st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

        # Option to switch to the next eligible formula
        next_formula = None
        for key, values in loan_formulas.items():
            if key != selected_formula and key.startswith("C") and (purchase_price * (1 - values["down_payment"] / 100)) <= loan_limits[num_units]["conforming"]:
                next_formula = key
                break

        if next_formula:
            new_cash_to_close_next = total_sale_price * (loan_formulas[next_formula]["down_payment"] / 100)
            if st.button(f"🔄 Switch to {next_formula} (Eligible Formula)\nTotal Cash to Close: ${new_cash_to_close_next:,.2f}"):
                st.write("")  # Clear original results
                selected_formula = next_formula
                down_payment_pct = loan_formulas[next_formula]["down_payment"] / 100
                total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
                    purchase_price, loan_term, interest_rate, down_payment_pct, loan_formulas[next_formula]["seller_concession"] / 100, property_tax, home_insurance, flood_insurance
                )

                if total_sale_price and loan_amount and cash_to_close and monthly_payment and total_monthly_payment:
                    st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
                    st.write(f"Loan Amount: ${loan_amount:,.2f}")
                    st.write(f"Cash to Close: ${cash_to_close:,.2f}")
                    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
                    st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

    # Validate high balance formulas
    elif selected_formula.startswith("HB") and (loan_amount <= loan_limits[num_units]["conforming"] or loan_amount > loan_limits[num_units]["high_balance"]):
        st.markdown(f'<div style="background-color:red; color:white; padding:10px; font-size:16px;">'
                    f'<strong>Loan amount (${loan_amount:,.2f}) exceeds the high-balance limit for {num_units}-unit property (${loan_limits[num_units]["high_balance"]:,.2f}) or is below the conforming limit (${loan_limits[num_units]["conforming"]:,.2f}).</strong></div>',
                    unsafe_allow_html=True)

        # Hide original results
        st.write("")
        st.write("")

        next_formula = None
        for key, values in loan_formulas.items():
            if key != selected_formula and key.startswith("HB") and (loan_limits[num_units]["conforming"] < purchase_price * (1 - values["down_payment"] / 100) <= loan_limits[num_units]["high_balance"]):
                next_formula = key
                break

        if next_formula:
            new_cash_to_close_next = total_sale_price * (loan_formulas[next_formula]["down_payment"] / 100)
            if st.button(f"🔄 Switch to {next_formula} (Eligible Formula)\nTotal Cash to Close: ${new_cash_to_close_next:,.2f}"):
                st.write("")  # Clear original results
                selected_formula = next_formula
                down_payment_pct = loan_formulas[next_formula]["down_payment"] / 100
                total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
                    purchase_price, loan_term, interest_rate, down_payment_pct, loan_formulas[next_formula]["seller_concession"] / 100, property_tax, home_insurance, flood_insurance
                )

                if total_sale_price and loan_amount and cash_to_close and monthly_payment and total_monthly_payment:
                    st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
                    st.write(f"Loan Amount: ${loan_amount:,.2f}")
                    st.write(f"Cash to Close: ${cash_to_close:,.2f}")
                    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
                    st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

    # Check if the loan amount exceeds the max loan limit
    if loan_amount > max_loan_limit:
        st.markdown(f'<div style="background-color:red; color:white; padding:10px; font-size:16px;">'
                    f'<strong>{selected_formula} is ineligible because the loan amount (${loan_amount:,.2f}) exceeds the max loan limit (${max_loan_limit:,.2f}).</strong></div>',
                    unsafe_allow_html=True)

        # Hide original results
        st.write("")
        st.write("")

        adjusted_down_payment = ((loan_amount - max_loan_limit) / total_sale_price * 100) + loan_formulas[selected_formula]["down_payment"]
        new_cash_to_close = total_sale_price * (adjusted_down_payment / 100)

        st.session_state.adjusted_down_payment = adjusted_down_payment
        st.session_state.new_cash_to_close = new_cash_to_close

        if st.button(f"✅ Apply {adjusted_down_payment:.2f}% Down Payment & Recalculate\nTotal Cash to Close: ${new_cash_to_close:,.2f}"):
            st.write("")  # Clear original results
            down_payment_pct = adjusted_down_payment / 100
            total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
                purchase_price, loan_term, interest_rate, down_payment_pct, seller_concession_pct, property_tax, home_insurance, flood_insurance
            )

            if total_sale_price and loan_amount and cash_to_close and monthly_payment and total_monthly_payment:
                st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
                st.write(f"Loan Amount: ${loan_amount:,.2f}")
                st.write(f"Cash to Close: ${cash_to_close:,.2f}")
                st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
                st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")

        next_formula = None
        for key, values in loan_formulas.items():
            if key != selected_formula and (purchase_price * (1 - values["down_payment"] / 100)) <= max_loan_limit:
                next_formula = key
                break

        if next_formula:
            new_cash_to_close_next = total_sale_price * (loan_formulas[next_formula]["down_payment"] / 100)
            if st.button(f"🔄 Switch to {next_formula} (Eligible Formula)\nTotal Cash to Close: ${new_cash_to_close_next:,.2f}"):
                st.write("")  # Clear original results
                selected_formula = next_formula
                down_payment_pct = loan_formulas[next_formula]["down_payment"] / 100
                total_sale_price, loan_amount, cash_to_close, monthly_payment, total_monthly_payment = calculate_loan(
                    purchase_price, loan_term, interest_rate, down_payment_pct, loan_formulas[next_formula]["seller_concession"] / 100, property_tax, home_insurance, flood_insurance
                )

                if total_sale_price and loan_amount and cash_to_close and monthly_payment and total_monthly_payment:
                    st.write(f"Total Sale Price: ${total_sale_price:,.2f}")
                    st.write(f"Loan Amount: ${loan_amount:,.2f}")
                    st.write(f"Cash to Close: ${cash_to_close:,.2f}")
                    st.write(f"Monthly Payment: ${monthly_payment:,.2f}")
                    st.write(f"Total Monthly Payment (Including Taxes & Insurance): ${total_monthly_payment:,.2f}")
