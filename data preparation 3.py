import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Users\arnel\OneDrive - KU Leuven\Thesis Economics\Python\Data\prepared data 2.csv', parse_dates=['IPO date'])

# Convert numerical columns to numerical data type
numerical_columns = [
    "Market capitalization (m)", "Net profit (th)", "ROE", "Price / book value",
    "Shares outstanding (th)", "EPS", "P/E", "Total assets (th)", "Net debt (th)",
    "Cash & cash equivalent (th)", "Total debt (th)", "Total debt / Total assets", "Sales (th)"]

for column in numerical_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce')

# Drop rows where Sales = 0
df = df.loc[df['Sales (th)'] != 0]

# Count nan values for the rows
nan_counts_row = []

for index, row in df.iterrows():
    nan_count = row[numerical_columns].isna().sum()
    nan_counts_row.append((index, nan_count))

nan_counts_df = pd.DataFrame(nan_counts_row, columns=['Row Index', 'NaN Count'])

# Plot the occurence of the values of the nan values in a row  
nan_count_occurrences = nan_counts_df['NaN Count'].value_counts()
plt.figure(figsize=(10, 6))
nan_count_occurrences.plot(kind='bar')
plt.title('Occurrences of NaN Counts')
plt.xlabel('Number of NaNs in a Row')
plt.ylabel('Occurrences')
plt.xticks(rotation=0)
plt.show()

# Drop the rows with nan values since we still keep about 250 datapoints
df = df.dropna(subset=numerical_columns)
print(df.shape)

# Check balance of dataset
category_counts = df['Country'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
plt.xlabel('Category', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.title('Count of Categorical Values', fontsize=16)
plt.xticks(rotation=90, fontsize=12) 
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# Export csv files
df.to_csv(r'C:\Users\arnel\OneDrive - KU Leuven\Thesis Economics\Python\Data\prepared data 3.csv', index=False)
df.to_csv(r'C:\Users\arnel\thesis\CSV FILES\prepared data 3.csv', index=False)
print('prepared data 3 = ready')