import requests
import streamlit as st

st.title("Loan Default Risk Predictor")
st.write("Enter applicant details to assess default risk.")

API_URL = "https://angjinwei.app.n8n.cloud/webhook/loan-default-risk-predictor"

revolving_util = st.slider("Revolving Utilization of Unsecured Lines", 0.0, 1.5, 0.5)
age = st.number_input("Age", min_value=18, max_value=110, value=40)

late_30_59 = st.number_input("Times 30-59 Days Past Due", min_value=0, value=0)
late_60_89 = st.number_input("Times 60-89 Days Past Due", min_value=0, value=0)
late_90 = st.number_input("Times 90+ Days Late", min_value=0, value=0)

debt_ratio = st.number_input("Debt Ratio", min_value=0.0, value=0.3)


income = st.number_input("Monthly Income", min_value=0.0, value=1000.0)

open_credit_lines = st.number_input(
    "Number of Open Credit Lines and Loans", min_value=0, value=5
)
real_estate_loans = st.number_input(
    "Number of Real Estate Loans or Lines", min_value=0, value=1
)

dependents = st.number_input("Number of Dependents", min_value=0, value=0)

if st.button("Assess Risk"):
    payload = {
        "RevolvingUtilizationOfUnsecuredLines": revolving_util,
        "age": age,
        "NumberOfTime30to59DaysPastDueNotWorse": late_30_59,
        "DebtRatio": debt_ratio,
        "MonthlyIncome": income,
        "NumberOfOpenCreditLinesAndLoans": open_credit_lines,
        "NumberOfTimes90DaysLate": late_90,
        "NumberRealEstateLoansOrLines": real_estate_loans,
        "NumberOfTime60to89DaysPastDueNotWorse": late_60_89,
        "NumberOfDependents": dependents,
    }

    res = requests.post(API_URL, json=payload)

    if res.status_code == 200:
        result = res.json()
        risk_pct = result["risk_probability"] * 100

        if result["default_prediction"] == 1:
            st.error(f"High Risk — Estimated default probability: {risk_pct:.1f}%")
            st.info(result["recommendation"])
        else:
            st.success(f"Low Risk — Estimated default probability: {risk_pct:.1f}%")
            st.info(result["recommendation"])
    else:
        st.error(f"API error: {res.status_code} — {res.text}")
