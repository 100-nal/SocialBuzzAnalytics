import matplotlib.pyplot as plt
import pandas as pd
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

# Display the first few rows to ensure the merge was successful
print(merged_data.head())

# Drop irrelevant or duplicate columns, if any
merged_data_cleaned = merged_data.drop(columns=['UserID', 'Consumer ID'], errors='ignore')

# Display cleaned data
print(merged_data_cleaned.head())

platform_by_age = merged_data_cleaned.groupby('age')['Social Media Platforms'].value_counts()
print(platform_by_age)

usage_by_gender = merged_data_cleaned.groupby('gender')['Social Media Usage (Hours/Day)'].mean()
print(usage_by_gender)

influence_vs_spending = merged_data_cleaned.groupby('Influence Level')['Amount Spent (USD)'].mean()
print(influence_vs_spending)

# Plot average usage by gender
usage_by_gender.plot(kind='bar', title='Average Social Media Usage by Gender')
plt.ylabel('Hours per Day')
plt.show()

# Split and count platforms
platforms = merged_data_cleaned['Social Media Platforms'].str.split(', ').explode()
platform_counts = platforms.value_counts()

# Plot pie chart
platform_counts.plot(kind='pie', autopct='%1.1f%%', title='Popular Social Media Platforms')
plt.ylabel('')  # Hide y-axis label for clarity
plt.show()

influence_vs_spending.plot(kind='line', marker='o', title='Influence Level vs. Spending Behavior')
plt.ylabel('Average Amount Spent (USD)')
plt.xlabel('Influence Level')
plt.show()

merged_data_cleaned.to_csv('merged_social_media_data.csv', index=False)
