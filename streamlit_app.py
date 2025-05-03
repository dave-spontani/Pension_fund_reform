import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Streamlit App Title
st.title("Swiss Pension Fund Growth Simulator")

# Sidebar Inputs
starting_salary = st.sidebar.slider("Starting Monthly Salary (Brutto CHF)", 3000, 15000, 5000, step=100)
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


fig = go.Figure()

# Add one trace per interest rate
for col in df.columns:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[col],
        mode='lines+markers+text',
        name=col,
        text=[f"{val:,.0f} CHF" if i == len(df) - 1 else "" for i, val in enumerate(df[col])],
        textposition="top right"
    ))

fig.update_layout(
    title="Pension Fund Growth Over Time",
    xaxis_title="Age",
    yaxis_title="Total Pension Savings (CHF)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Calculate and display difference between 2% and 4% return scenarios
final_2 = df["2.0%"].iloc[-1]
final_3 = df["3.0%"].iloc[-1]
final_4 = df["4.0%"].iloc[-1]
final_5 = df["5.0%"].iloc[-1]

diff3_2 = final_3 - final_2

diff4_2 = final_4 - final_2

diff5_2 = final_5 - final_2


st.markdown(f"""
### 💰 Difference Between 2% and 3% Return Scenarios
If your pension fund earns **3% annually** (CHF {final_3:,.0f}) instead of **2%** (CHF {final_2:,.0f}), you would retire with approximately **CHF {diff3_2:,.0f}** more.
""")

st.markdown(f"""
### 💰 Difference Between 2% and 4% Return Scenarios
If your pension fund earns **4% annually** (CHF {final_4:,.0f}) instead of **2%** (CHF {final_2:,.0f}), you would retire with approximately **CHF {diff4_2:,.0f}** more.
""")

st.markdown(f"""
### 💰 Difference Between 2% and 5% Return Scenarios
If your pension fund earns **5% annually** (CHF {final_5:,.0f}) instead of **2%** (CHF {final_2:,.0f}), you would retire with approximately **CHF {diff5_2:,.0f}** more.
""")

# Optionally: Show raw data
with st.expander("Show data table"):
    st.dataframe(df)
