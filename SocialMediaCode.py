import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
from scipy.stats import f_oneway
import openpyxl

# Load the datasets
csv_data = pd.read_csv('Time-Wasters on Social Media.csv')
excel_data = pd.ExcelFile('Social Meida Dataset.xlsx')

# Parse the Excel file's first sheet
excel_data_sheet1 = excel_data.parse('Sheet1')

# Standardize column names for consistency
csv_data.rename(columns={'Age': 'age', 'Gender': 'gender'}, inplace=True)
excel_data_sheet1.rename(columns={'Age': 'age', 'Gender': 'gender'}, inplace=True)

# Merge datasets on age and gender
merged_data = pd.merge(csv_data, excel_data_sheet1, on=['age', 'gender'], how='inner')

# Drop irrelevant or duplicate columns, if any
merged_data_cleaned = merged_data.drop(columns=['UserID', 'Consumer ID'], errors='ignore')

# Save the cleaned merged data to a CSV file
output_file = 'merged_social_media_data.csv'
merged_data_cleaned.to_csv(output_file, index=False)

# Display confirmation and the first few rows
print(f"Merged data saved as '{output_file}'")
print(merged_data_cleaned.head())

# ---- ANALYSIS 1: Platform Popularity ----
platforms = merged_data_cleaned['Social Media Platforms'].str.split(', ').explode()
platform_counts = platforms.value_counts()

# Plot Platform Popularity
plt.figure(figsize=(8, 8))
platform_counts.plot(kind='pie', autopct='%1.1f%%', title='Popular Social Media Platforms', colors=plt.cm.Paired.colors)
plt.ylabel('')  # Hide y-axis label for clarity
plt.show()

# ---- ANALYSIS 2: Average Social Media Usage by Gender ----
usage_by_gender = merged_data_cleaned.groupby('gender')['Social Media Usage (Hours/Day)'].mean()
print("Average Social Media Usage by Gender:")
print(usage_by_gender)

# Plot Average Usage by Gender
plt.figure(figsize=(8, 6))
usage_by_gender.plot(kind='bar', title='Average Social Media Usage by Gender', color='skyblue')
plt.ylabel('Hours per Day')
plt.xlabel('Gender')
plt.show()

# ---- ANALYSIS 3: Spending by Influence Level ----
influence_vs_spending = merged_data_cleaned.groupby('Influence Level')['Amount Spent (USD)'].mean()
print("Spending by Influence Level:")
print(influence_vs_spending)

# Plot Influence Level vs. Spending
plt.figure(figsize=(8, 6))
influence_vs_spending.plot(kind='line', marker='o', title='Influence Level vs. Spending Behavior', color='green')
plt.ylabel('Average Amount Spent (USD)')
plt.xlabel('Influence Level')
plt.show()

# ---- ANALYSIS 4: Spending by Influence Level and Product Category ----
plt.figure(figsize=(10, 6))
sns.barplot(data=merged_data_cleaned, x="Influence Level", y="Amount Spent (USD)", hue="Product Category", palette="Set2")
plt.title("Spending by Influence Level and Product Category")
plt.xticks(rotation=45)
plt.ylabel("Amount Spent (USD)")
plt.show()

# ---- ANALYSIS 5: Interactive Scatter Plot: Social Media Usage vs Spending ----
fig = px.scatter(
    merged_data_cleaned,
    x="Social Media Usage (Hours/Day)",
    y="Amount Spent (USD)",
    color="Social Media Platforms",
    size="Amount Spent (USD)",
    hover_data=['gender', 'Influence Level'],
    title="Social Media Usage vs Spending Behavior",
    template="plotly_white"
)
fig.show()

# ---- ANALYSIS 6: Platform Usage by Gender (Cross-tabulation) ----
platforms_reset = platforms.reset_index(drop=True)
genders = merged_data_cleaned['gender'].repeat(merged_data_cleaned['Social Media Platforms'].str.split(', ').apply(len)).reset_index(drop=True)

crosstab = pd.crosstab(genders, platforms_reset)
print("Platform Usage by Gender:")
print(crosstab)

# Plot Platform Usage by Gender
plt.figure(figsize=(10, 6))
crosstab.plot(kind='bar', stacked=True, title='Platform Usage by Gender', figsize=(10, 6), colormap="viridis")
plt.ylabel('Count')
plt.xlabel('Gender')
plt.show()

# ---- ANALYSIS 7: ANOVA Test: Influence Level vs. Spending ----
anova = f_oneway(
    merged_data_cleaned[merged_data_cleaned['Influence Level'] == 'Very Influential']['Amount Spent (USD)'],
    merged_data_cleaned[merged_data_cleaned['Influence Level'] == 'Somewhat Influential']['Amount Spent (USD)'],
    merged_data_cleaned[merged_data_cleaned['Influence Level'] == 'Not Influential']['Amount Spent (USD)']
)
print(f"ANOVA Test Result: F-statistic = {anova.statistic:.2f}, p-value = {anova.pvalue:.4f}")

# ---- ANALYSIS 8: Spending Trends by Age ----
spending_by_age = merged_data_cleaned.groupby('age')['Amount Spent (USD)'].mean()
print("Spending Trends by Age:")
print(spending_by_age)

# Plot Spending Trends by Age
plt.figure(figsize=(10, 6))
spending_by_age.plot(kind='line', marker='o', title='Spending Trends by Age', color='red')
plt.ylabel('Average Amount Spent (USD)')
plt.xlabel('Age')
plt.grid()
plt.show()

# ---- Additional Insights: Usage vs Spending Correlation ----
correlation = merged_data_cleaned['Social Media Usage (Hours/Day)'].corr(merged_data_cleaned['Amount Spent (USD)'])
print(f"Correlation between Social Media Usage and Spending: {correlation:.2f}")

# ---- Save Cleaned Data ----
merged_data_cleaned.to_csv('merged_social_media_data.csv', index=False)
print("Cleaned and merged data saved as 'merged_social_media_data.csv'")

