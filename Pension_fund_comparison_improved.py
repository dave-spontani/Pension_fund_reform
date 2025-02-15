import numpy as np
import matplotlib.pyplot as plt

# Constants
starting_salary = 5000  # CHF per month
salary_growth_rate = 0.02  # 2% annual salary growth
retirement_age = 61
current_age = 25
months_per_year = 12

# BVG contribution rates by age bracket (total % of insured salary)
bvg_rates = {
    (25, 34): 0.07,
    (35, 44): 0.10,
    (45, 54): 0.15,
    (55, 65): 0.18,
}

# Coordination deduction (fixed for 2024)
coordination_deduction = 25725  # Annual deduction

# Interest rate scenarios
interest_rates = [0.0125, 0.02, 0.025, 0.03, 0.035, 0.04, 0.06]  # 2%, 4%, 6% annual return

# Initialize savings, contributions, and salary tracker
savings_over_time = {r: [] for r in interest_rates}
annual_contributions = []
salary_over_time = []

def get_bvg_rate(age):
    for (start, end), rate in bvg_rates.items():
        if start <= age <= end:
            return rate
    return 0.07  # Default to the lowest if undefined

# Simulation loop
savings = {r: 0.0 for r in interest_rates}
salary = starting_salary

for age in range(current_age, retirement_age):
    salary_over_time.append(round(salary))
    insured_salary = max(0, (salary * months_per_year) - coordination_deduction)
    contribution_rate = get_bvg_rate(age)
    annual_contribution = insured_salary * contribution_rate
    annual_contributions.append(round(annual_contribution))
    
    for r in interest_rates:
        savings[r] += annual_contribution  # Add contributions
        savings[r] *= (1 + r)  # Apply investment growth
        savings_over_time[r].append(round(savings[r]))
    
    salary *= (1 + salary_growth_rate)  # Apply salary growth

# Plot results
plt.figure(figsize=(10, 6))
for r in interest_rates:
    plt.plot(range(current_age, retirement_age), savings_over_time[r], label=f"{round(float(r*100),2)}% Return", marker="o",)
    
plt.xlabel("Age")
plt.ylabel("Total Pension Savings (CHF)")
plt.title("Pension Fund Growth Over Time")
plt.legend()
plt.grid()
plt.show()

# Plot annual contributions
plt.figure(figsize=(10, 6))
plt.plot(range(current_age, retirement_age), annual_contributions, label="Annual Contributions",marker="o", color='red')
plt.xlabel("Age")
plt.ylabel("Annual Contribution (CHF)")
plt.title("Annual Pension Fund Contributions Over Time")
plt.legend()
plt.grid()
plt.show()

# Plot salary evolution
plt.figure(figsize=(10, 6))
plt.plot(range(current_age, retirement_age), salary_over_time, label="Salary Evolution",marker="o", color='blue')
plt.xlabel("Age")
plt.ylabel("Salary (CHF)")
plt.title("Salary Growth Over Time")
plt.legend()
plt.grid()
plt.show()

print(salary_over_time)

print(annual_contributions)

print(savings_over_time)