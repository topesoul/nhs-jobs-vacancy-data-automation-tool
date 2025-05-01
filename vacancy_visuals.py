import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import re
from fuzzywuzzy import process

# Load the CSV file
data = pd.read_csv(r'C:\\Script\\nhs_jobs_report_2024-10-07_095930.csv')

# Function to remove postcodes and specific address patterns to reduce duplication
def remove_postcode(location):
    # This regex will remove common postcode patterns and clean specific patterns like road names, unit numbers, etc.
    return re.sub(r'\b[A-Z]{1,2}\d{1,2}\s?\d?[A-Z]{1,2}\b|\d+|road|avenue|street|drive|lane|unit|suite|building', '', location, flags=re.IGNORECASE).strip()

# Clean Location Data: remove postcodes, address patterns, and apply proper title case
data['Location'] = data['Location'].apply(remove_postcode).str.strip().str.title()

# Apply fuzzy matching for similar locations
def match_locations(location, choices, threshold=90):
    match, score = process.extractOne(location, choices)
    return match if score >= threshold else location

# Get the unique location names to match against
unique_locations = data['Location'].unique()

# Apply fuzzy matching to the entire dataset
data['Location'] = data['Location'].apply(lambda x: match_locations(x, unique_locations))

# 1. Job Distribution by Employer (Interactive with Plotly)
employer_counts = data['Employer'].value_counts().reset_index()
employer_counts.columns = ['Employer', 'Vacancies']
fig = px.bar(employer_counts, x='Vacancies', y='Employer', orientation='h', title='Job Distribution by Employer')
fig.show()

# 2. Donut Chart for Contract Type Breakdown (Using Plotly)
contract_type_counts = data['Contract Type'].value_counts().reset_index()
contract_type_counts.columns = ['Contract Type', 'Count']
fig = px.pie(contract_type_counts, names='Contract Type', values='Count', hole=0.4, title='Contract Type Breakdown (Donut Chart)')
fig.show()

# 3. Vacancy Trends Over Time (Interactive Line Chart)
data['Post Date'] = pd.to_datetime(data['Post Date'], errors='coerce')  # Convert Post Date to datetime
post_date_counts = data['Post Date'].dt.date.value_counts().reset_index()
post_date_counts.columns = ['Post Date', 'Vacancies']
post_date_counts = post_date_counts.sort_values('Post Date')

fig = px.line(post_date_counts, x='Post Date', y='Vacancies', title='Vacancy Posting Trends Over Time')
fig.show()

# 4. Top 10 Locations for Vacancies (Interactive)
location_counts = data['Location'].value_counts().reset_index().head(10)
location_counts.columns = ['Location', 'Vacancies']

fig = px.bar(location_counts, x='Vacancies', y='Location', orientation='h', title='Top 10 Locations for Vacancies')
fig.show()

# 5. Salary Range Cleaning
data['Min Salary'] = data['Salary Range'].str.extract(r'£(\d+.\d+)').astype(float)
data['Max Salary'] = data['Salary Range'].str.extract(r'to £(\d+.\d+)').astype(float)

# Calculate Mean Salary
data['Mean Salary'] = (data['Min Salary'] + data['Max Salary']) / 2

# 6. Salary Range Distribution with Mean Salary (using Matplotlib)
plt.figure(figsize=(10, 6))

# Plot histogram for Min and Max Salary
plt.hist([data['Min Salary'], data['Max Salary']], bins=20, label=['Min Salary', 'Max Salary'], color=['lightcoral', 'lightgreen'], alpha=0.6)

# Plot the distribution for Mean Salary as a line
mean_salary_vals = data['Mean Salary'].dropna()
plt.axvline(mean_salary_vals.mean(), color='blue', linestyle='dashed', linewidth=2, label=f'Mean Salary: £{mean_salary_vals.mean():,.2f}')

plt.title('Salary Range Distribution with Mean Salary')
plt.xlabel('Salary (£)')
plt.ylabel('Number of Vacancies')
plt.legend()
plt.tight_layout()
plt.show()