
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from matplotlib.gridspec import GridSpec

# Load the dataset
data = pd.read_csv("DataScience_salaries_2024.csv")
data = data.sort_values(by="salary_in_usd", ascending=False)

# Recode categorical values
exp_map = {'MI': 'Mid-Level', 'EN': 'Entry-Level', 'SE': 'Senior', 'EX': 'Expert'}
emp_type_map = {'FT': "Full-Time", 'PT': "Part-Time", 'CT': "Contract"}
company_size_map = {'S': 'Small', 'L': 'Large', 'M': 'Medium'}

data['experience_level'] = data['experience_level'].map(exp_map)
data['employment_type'] = data['employment_type'].map(emp_type_map)
data['company_size'] = data['company_size'].map(company_size_map)

# Drop NA
data = data.dropna()

# Group job titles
top_jobs = data['job_title'].value_counts().nlargest(10).index
data['job_title_grouped'] = data['job_title'].apply(lambda x: x if x in top_jobs else 'Other')

# Aggregated data for plotting
df_salary_company = data.groupby("company_size", as_index=False)["salary_in_usd"].mean()
df_heatmap = data.groupby(["job_title_grouped", "experience_level"], as_index=False)["salary_in_usd"].mean()
df_line = data.groupby(["work_year", "company_size"], as_index=False)["salary_in_usd"].mean()
heatmap_data = df_heatmap.pivot(index="job_title_grouped", columns="experience_level", values="salary_in_usd")

# Create 2x2 grid of plots
fig = plt.figure(constrained_layout=True, figsize=(16, 12))
gs = GridSpec(2, 2, figure=fig)

# Plot 1
ax1 = fig.add_subplot(gs[0, 0])
sns.histplot(data=data, x="salary_in_usd", hue="job_title_grouped", binwidth=20000,
             multiple="stack", palette="Set3", edgecolor="black", alpha=0.7, ax=ax1)
ax1.set_title("A. Salary Distribution by Job Title Grouped")
ax1.set_xlabel("Salary in USD")
ax1.set_ylabel("Count")

# Plot 2
ax2 = fig.add_subplot(gs[0, 1])
sns.barplot(data=df_salary_company, x="company_size", y="salary_in_usd", palette="Blues_d", ax=ax2)
ax2.set_title("B. Avg Salary by Company Size")
ax2.set_ylabel("Average Salary (USD)")
ax2.set_xlabel("Company Size")
ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:,.0f}'))

# Plot 3
ax3 = fig.add_subplot(gs[1, 0])
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Blues", linewidths=0.5,
            cbar_kws={'label': 'Avg Salary (USD)'}, ax=ax3)
ax3.set_title("C. Avg Salary by Title and Experience")
ax3.set_xlabel("Experience Level")
ax3.set_ylabel("Job Title Grouped")

# Plot 4
ax4 = fig.add_subplot(gs[1, 1])
sns.lineplot(data=df_line, x="work_year", y="salary_in_usd", hue="company_size",
             marker="o", palette="Dark2", ax=ax4)
ax4.set_title("D. Salary Trend Over Years by Company Size")
ax4.set_xlabel("Work Year")
ax4.set_ylabel("Average Salary (USD)")
ax4.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax4.legend(title="Company Size")

plt.show()
