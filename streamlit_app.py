import streamlit as st
import numpy as np
import pandas as pd

# Streamlit App Title
st.title("Swiss Pension Fund Growth Simulator")

# Sidebar Inputs
starting_salary = st.sidebar.slider("Starting Monthly Salary (CHF)", 3000, 15000, 5000, step=100)
salary_growth_rate = st.sidebar.slider("Annual Salary Growth Rate (%)", 0.0, 5.0, 2.0, step=0.1) / 100
current_age = st.sidebar.slider("Current Age", 20, 60, 25)
retirement_age = 65

# Constants
months_per_year = 12
coordination_deduction = 25725  # Fixed for 2024
interest_rates = [0.0125, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05]

bvg_rates = {
    (25, 34): 0.07,
    (35, 44): 0.10,
    (45, 54): 0.15,
    (55, 65): 0.18,
}

def get_bvg_rate(age):
    for (start, end), rate in bvg_rates.items():
        if start <= age <= end:
            return rate
    return 0.07

# Initialize trackers
savings = {r: 0.0 for r in interest_rates}
savings_over_time = {r: [] for r in interest_rates}
salary = starting_salary

# Simulation loop
for age in range(current_age, retirement_age):
    insured_salary = max(0, (salary * months_per_year) - coordination_deduction)
    contribution_rate = get_bvg_rate(age)
    annual_contribution = insured_salary * contribution_rate

    for r in interest_rates:
        savings[r] += annual_contribution
        savings[r] *= (1 + r)
        savings_over_time[r].append(round(savings[r]))

    salary *= (1 + salary_growth_rate)

# Build DataFrame for plotting
ages = list(range(current_age, retirement_age))
df = pd.DataFrame({f"{round(r * 100, 2)}%": savings_over_time[r] for r in interest_rates}, index=ages)
df.index.name = "Age"

# Display interactive chart
st.line_chart(df)

# Optionally: Show raw data
with st.expander("Show data table"):
    st.dataframe(df)
