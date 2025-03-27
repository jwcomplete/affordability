
import streamlit as st

st.set_page_config(page_title="Build Your Profile", layout="wide")

# Custom CSS for input widths and styling placeholders
st.markdown("""
    <style>
    div[data-baseweb="input"] input {
        max-width: 400px;
    }
    .stNumberInput input {
        width: 200px;
        padding-left: 20px;
    }
    div[data-baseweb="select"] {
        max-width: 180px;
    }
    .stNumberInput input::placeholder {
        color: gray;
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript to handle placeholder behavior
st.markdown("""
    <script>
    const elements = document.querySelectorAll('.stNumberInput input');
    elements.forEach(el => {
        el.onfocus = function() {
            if (this.value === "$0.00") {
                this.value = "";
            }
        };
        el.onblur = function() {
            if (this.value === "") {
                this.value = "$0.00";
            }
        };
    });
    </script>
""", unsafe_allow_html=True)

st.title("📄 Build Your Profile")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🧍 Personal Details")
    first_name = st.text_input("First Name", max_chars=50)
    last_name = st.text_input("Last Name", max_chars=50)

    st.markdown("### 🏡 Subject Property")
    property_address = st.text_input("Property Address", max_chars=75)

    col_val, col_occ, col_flood, col_units = st.columns([2.5, 2, 1.5, 1])
    with col_val:
        st.markdown("**Estimated Value ($)**")
        estimated_value = st.number_input("", min_value=0.0, max_value=9999999999.00, step=1000.0, format="%0.2f", value=0.00, key="estimated_value", help="Enter the estimated value")
    with col_occ:
        occupancy_type = st.selectbox("Intended Occupancy", ["Owner-Occupied", "Second Home", "Investment"])
    with col_flood:
        flood_zone = st.selectbox("Flood Zone", ["Yes", "No"], key="flood_zone")
    with col_units:
        num_units = st.selectbox("# of Units", [1, 2, 3, 4], key="num_units")

    st.markdown("### 🏘️ Accessory Unit")
    col_acc_q, col_acc_a = st.columns([3, 1])
    with col_acc_q:
        st.markdown("**Does the property have an accessory unit?**")
    with col_acc_a:
        accessory_unit = st.selectbox(" ", ["No", "Yes"], key="accessory_unit")

    if accessory_unit == "Yes":
        col_sep_q, col_sep_a = st.columns([3, 1])
        with col_sep_q:
            st.markdown("**Interior separation from primary unit?**")
        with col_sep_a:
            interior_separation = st.selectbox(" ", ["No", "Yes"], key="interior_separation")
        col_kitch_q, col_kitch_a = st.columns([3, 1])
        with col_kitch_q:
            st.markdown("**Kitchen with fridge, stove, sink?**")
        with col_kitch_a:
            has_kitchen = st.selectbox(" ", ["No", "Yes"], key="has_kitchen")
        col_bath_q, col_bath_a = st.columns([3, 1])
        with col_bath_q:
            st.markdown("**Bathroom present?**")
        with col_bath_a:
            has_bathroom = st.selectbox(" ", ["No", "Yes"], key="has_bathroom")

        if all(ans == "Yes" for ans in [interior_separation, has_kitchen, has_bathroom]) and num_units == 1:
            st.markdown("**Proposed Market Rent for Accessory Unit ($)**")
            proposed_rent = st.number_input("", min_value=0.0, format="%0.2f", value=0.00, key="proposed_rent", help="Enter the proposed market rent")

with col2:
    st.markdown("### 💵 Financial Information")
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        st.markdown("**Cash Available to Close ($)**")
        cash_available = st.number_input("", min_value=0.0, max_value=9999999999.00, step=1000.0, format="%0.2f", value=0.00, key="cash_available", help="Enter the cash available to close")
        st.markdown("**Included Monthly Debts ($)**")
        monthly_debts = st.number_input("", min_value=0.0, max_value=9999999999.00, step=100.0, format="%0.2f", value=0.00, key="monthly_debts", help="Enter the included monthly debts")
    with col_f2:
        st.markdown("**Qualifying Income ($/year)**")
        qualifying_income = st.number_input("", min_value=0.0, max_value=9999999999.00, step=1000.0, format="%0.2f", value=0.00, key="qualifying_income", help="Enter the qualifying income")

st.button("✅ Save Profile")
