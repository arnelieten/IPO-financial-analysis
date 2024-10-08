import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Users\arnel\OneDrive - KU Leuven\Thesis Economics\Python\Data\prepared data 1.csv', parse_dates=['IPO date'])

# Assign right Market capitalization
def select_market_cap(row):
    year = row['IPO date'].year
    cap_column = f"Market capitalisation\nm EUR {year}"
    return row.get(cap_column, pd.NA)

df['Market capitalization (m)'] = df.apply(select_market_cap, axis=1)
df['Market capitalization (m)'] = df['Market capitalization (m)'].str.replace(',', '')
df['Market capitalization (m)'] = pd.to_numeric(df['Market capitalization (m)'], errors='coerce')

# Remove helper columns
df = df.drop('Market capitalisation\nm EUR 2024', axis=1)
df = df.drop('Market capitalisation\nm EUR 2023', axis=1)
df = df.drop('Market capitalisation\nm EUR 2022', axis=1)
df = df.drop('Market capitalisation\nm EUR 2021', axis=1)
df = df.drop('Market capitalisation\nm EUR 2020', axis=1)

# Assign right Net profit
def select_net_profit(row):
    year = row['IPO date'].year
    profit_column = f"Net profit\nth EUR {year}"
    return row.get(profit_column, pd.NA)

df['Net profit (th)'] = df.apply(select_net_profit, axis=1)
df['Net profit (th)'] = df['Net profit (th)'].str.replace(',', '')
df['Net profit (th)'] = pd.to_numeric(df['Net profit (th)'], errors='coerce')

# Remove helper columns
df = df.drop('Net profit\nth EUR 2023', axis=1)
df = df.drop('Net profit\nth EUR 2022', axis=1)
df = df.drop('Net profit\nth EUR 2021', axis=1)
df = df.drop('Net profit\nth EUR 2020', axis=1)

# Assign right ROE (year basis)
def select_roe_yearly(row):
    year = row['IPO date'].year
    roe_yearly_column = f"ROE using Net income\n{year}"
    return row.get(roe_yearly_column, pd.NA)

df['ROE (yearly)'] = df.apply(select_roe_yearly, axis=1)

# Remove helper columns
df = df.drop('ROE using Net income\n2023', axis=1)
df = df.drop('ROE using Net income\n2022', axis=1)
df = df.drop('ROE using Net income\n2021', axis=1)
df = df.drop('ROE using Net income\n2020', axis=1)

# Assign right ROE (quarter basis)
years = [2023, 2022, 2021, 2020]

for year in years:
    quarter_columns = [f'ROE using Net income\n{year} Quarter {i}' for i in range(1, 5)]
    df[quarter_columns] = df[quarter_columns].apply(pd.to_numeric, errors='coerce')
    df[f'ROE (quarterly) {year}'] = df[quarter_columns].mean(axis=1)

df['ROE (quarterly) 2023'] = df[['ROE using Net income\n2023 Quarter 1', 
                                 'ROE using Net income\n2023 Quarter 2', 
                                 'ROE using Net income\n2023 Quarter 3', 
                                 'ROE using Net income\n2023 Quarter 4']].mean(axis=1)

df['ROE (quarterly) 2022'] = df[['ROE using Net income\n2022 Quarter 1', 
                                 'ROE using Net income\n2022 Quarter 2', 
                                 'ROE using Net income\n2022 Quarter 3', 
                                 'ROE using Net income\n2022 Quarter 4']].mean(axis=1)

df['ROE (quarterly) 2021'] = df[['ROE using Net income\n2021 Quarter 1', 
                                 'ROE using Net income\n2021 Quarter 2', 
                                 'ROE using Net income\n2021 Quarter 3', 
                                 'ROE using Net income\n2021 Quarter 4']].mean(axis=1)

df['ROE (quarterly) 2020'] = df[['ROE using Net income\n2020 Quarter 1', 
                                 'ROE using Net income\n2020 Quarter 2', 
                                 'ROE using Net income\n2020 Quarter 3', 
                                 'ROE using Net income\n2020 Quarter 4']].mean(axis=1)

def select_roe_quarterly(row):
    year = row['IPO date'].year
    roe_quarterly_column = f"ROE (quarterly) {year}"
    return row.get(roe_quarterly_column, pd.NA)

df['ROE (quarterly)'] = df.apply(select_roe_quarterly, axis=1)

# Create ROE (ROE (yearly) > ROE (quarterly))
df['ROE (yearly)'] = pd.to_numeric(df['ROE (yearly)'], errors='coerce')
df['ROE (quarterly)'] = pd.to_numeric(df['ROE (quarterly)'], errors='coerce')
df['ROE'] = df['ROE (yearly)'].combine_first(df['ROE (quarterly)'])

# Remove helper columns
columns_to_drop_roe = [
    'ROE using Net income\n2023 Quarter 1',
    'ROE using Net income\n2023 Quarter 2',
    'ROE using Net income\n2023 Quarter 3',
    'ROE using Net income\n2023 Quarter 4',
    'ROE using Net income\n2022 Quarter 1',
    'ROE using Net income\n2022 Quarter 2',
    'ROE using Net income\n2022 Quarter 3',
    'ROE using Net income\n2022 Quarter 4',
    'ROE using Net income\n2021 Quarter 1',
    'ROE using Net income\n2021 Quarter 2',
    'ROE using Net income\n2021 Quarter 3',
    'ROE using Net income\n2021 Quarter 4',
    'ROE using Net income\n2020 Quarter 1',
    'ROE using Net income\n2020 Quarter 2',
    'ROE using Net income\n2020 Quarter 3',
    'ROE using Net income\n2020 Quarter 4',
    'ROE (quarterly) 2023',
    'ROE (quarterly) 2022',
    'ROE (quarterly) 2021',
    'ROE (quarterly) 2020',
    'ROE (quarterly)',
    'ROE (yearly)']
df.drop(columns=columns_to_drop_roe, inplace=True)

# Assign right price / book value (year basis)
years = range(2024, 2019, -1)

for year in years:
    column_name_close = f'Price / book value ratio - close\n{year}'
    df[column_name_close] = pd.to_numeric(df[column_name_close], errors='coerce')

    column_name_open = f'Price / book value ratio - open\n{year}'
    df[column_name_open] = pd.to_numeric(df[column_name_open], errors='coerce')

df['Price / book value ratio 2024'] = df[['Price / book value ratio - close\n2024', 
                                 'Price / book value ratio - open\n2024']].mean(axis=1)
df['Price / book value ratio 2023'] = df[['Price / book value ratio - close\n2023', 
                                 'Price / book value ratio - open\n2023']].mean(axis=1)
df['Price / book value ratio 2022'] = df[['Price / book value ratio - close\n2022', 
                                 'Price / book value ratio - open\n2022']].mean(axis=1)
df['Price / book value ratio 2021'] = df[['Price / book value ratio - close\n2021', 
                                 'Price / book value ratio - open\n2021']].mean(axis=1)
df['Price / book value ratio 2020'] = df[['Price / book value ratio - close\n2020', 
                                 'Price / book value ratio - open\n2020']].mean(axis=1)

def select_pb_yearly(row):
    year = row['IPO date'].year
    pb_yearly_column = f"Price / book value ratio {year}"
    return row.get(pb_yearly_column, pd.NA)

df['Price / book value'] = df.apply(select_pb_yearly, axis=1)

# Remove helper columns
columns_to_drop_pb_yearly = [
    'Price / book value ratio - close\n2024',
    'Price / book value ratio - open\n2024',
    'Price / book value ratio - close\n2023',
    'Price / book value ratio - open\n2023',
    'Price / book value ratio - close\n2022',
    'Price / book value ratio - open\n2022',
    'Price / book value ratio - close\n2021',
    'Price / book value ratio - open\n2021',
    'Price / book value ratio - close\n2020',
    'Price / book value ratio - open\n2020',
    'Price / book value ratio 2024',
    'Price / book value ratio 2023',
    'Price / book value ratio 2022',
    'Price / book value ratio 2021',
    'Price / book value ratio 2020']

df.drop(columns=columns_to_drop_pb_yearly, inplace=True)

# Assign right Shares outstanding
def select_shares_outstanding(row):
    initial_year = row['IPO date'].year
    years_to_check = [initial_year, initial_year + 1, initial_year - 1]
    
    for year in years_to_check:
        shares_column = f"Shares outstanding\nth {year}"
        value = row.get(shares_column)
        if pd.notna(value):
            return value.replace(',', '')
    return pd.NA

df['Shares outstanding (th)'] = df.apply(select_shares_outstanding, axis=1)
df['Shares outstanding (th)'] = pd.to_numeric(df['Shares outstanding (th)'], errors='coerce')

# Remove helper columns
df = df.drop('Shares outstanding\nth 2024', axis=1)
df = df.drop('Shares outstanding\nth 2023', axis=1)
df = df.drop('Shares outstanding\nth 2022', axis=1)
df = df.drop('Shares outstanding\nth 2021', axis=1)
df = df.drop('Shares outstanding\nth 2020', axis=1)

# Assign EPS (based on EPS data)
def select_eps_eps(row):
    year = row['IPO date'].year
    eps_eps_column = f"Earnings per share\nEUR {year}"
    return row.get(eps_eps_column, pd.NA)

df['EPS eps data'] = df.apply(select_eps_eps, axis=1)
df['EPS eps data'] = pd.to_numeric(df['EPS eps data'], errors='coerce')

# Assign EPS (based on earnings data)
df['EPS earnings data'] = df['Net profit (th)']/df['Shares outstanding (th)']

# Assign right EPS
df['EPS eps data'] = pd.to_numeric(df['EPS eps data'], errors='coerce')
df['EPS earnings data'] = pd.to_numeric(df['EPS earnings data'], errors='coerce')
df['EPS'] = df['EPS eps data'].combine_first(df['EPS earnings data'])

# Remove helper columns
columns_to_drop_eps = [
    'Earnings per share\nEUR 2024',
    'Earnings per share\nEUR 2023',
    'Earnings per share\nEUR 2022',
    'Earnings per share\nEUR 2021',
    'Earnings per share\nEUR 2020',
    'EPS eps data',
    'EPS earnings data']

df.drop(columns=columns_to_drop_eps, inplace=True)

# Assign P/E (based on P/E)
years = range(2024, 2019, -1)

for year in years:
    column_name_close_pe = f'Price / earnings ratio - close\n{year}'
    df[column_name_close_pe] = pd.to_numeric(df[column_name_close_pe], errors='coerce')

    column_name_open_pe = f'Price / earnings ratio - open\n{year}'
    df[column_name_open_pe] = pd.to_numeric(df[column_name_open_pe], errors='coerce')

df['P/E (based on P/E) 2024'] = df[['Price / earnings ratio - close\n2024', 
                                 'Price / earnings ratio - open\n2024']].mean(axis=1)
df['P/E (based on P/E) 2023'] = df[['Price / earnings ratio - close\n2023', 
                                 'Price / earnings ratio - open\n2023']].mean(axis=1)
df['P/E (based on P/E) 2022'] = df[['Price / earnings ratio - close\n2022', 
                                 'Price / earnings ratio - open\n2022']].mean(axis=1)
df['P/E (based on P/E) 2021'] = df[['Price / earnings ratio - close\n2021', 
                                 'Price / earnings ratio - open\n2021']].mean(axis=1)
df['P/E (based on P/E) 2020'] = df[['Price / earnings ratio - close\n2020', 
                                 'Price / earnings ratio - open\n2020']].mean(axis=1)

def select_pe_pe(row):
    year = row['IPO date'].year
    pe_pe_column = f"P/E (based on P/E) {year}"
    return row.get(pe_pe_column, pd.NA)

df['P/E (based on P/E)'] = df.apply(select_pe_pe, axis=1)

# Assign P/E (based on earnings)
df['P/E (based on earnings)'] = (df['Market capitalization (m)'] * 1000) / df['Net profit (th)']

# Assign right P/E
df['P/E (based on P/E)'] = pd.to_numeric(df['P/E (based on P/E)'], errors='coerce')
df['P/E (based on earnings)'] = pd.to_numeric(df['P/E (based on earnings)'], errors='coerce')
df['P/E'] = df['P/E (based on P/E)'].combine_first(df['P/E (based on earnings)'])

# Remove helper columns
columns_to_drop_pe = [
    "Price / earnings ratio - close\n2024",
    "Price / earnings ratio - close\n2023",
    "Price / earnings ratio - close\n2022",
    "Price / earnings ratio - close\n2021",
    "Price / earnings ratio - close\n2020",
    "Price / earnings ratio - open\n2024",
    "Price / earnings ratio - open\n2023",
    "Price / earnings ratio - open\n2022",
    "Price / earnings ratio - open\n2021",
    "Price / earnings ratio - open\n2020",
    "P/E (based on P/E) 2024",
    "P/E (based on P/E) 2023",
    "P/E (based on P/E) 2022",
    "P/E (based on P/E) 2021",
    "P/E (based on P/E) 2020",
    'P/E (based on P/E)',
    'P/E (based on earnings)']

df = df.drop(columns=columns_to_drop_pe)

# Assign Total assets
def select_total_assets(row):
    year = row['IPO date'].year
    total_assets_column = f"Total Assets\nth EUR {year}"
    return row.get(total_assets_column, pd.NA)

df['Total assets (th)'] = df.apply(select_total_assets, axis=1)

# Remove helper columns
df = df.drop('Total Assets\nth EUR 2023', axis=1)
df = df.drop('Total Assets\nth EUR 2022', axis=1)
df = df.drop('Total Assets\nth EUR 2021', axis=1)
df = df.drop('Total Assets\nth EUR 2020', axis=1)

# Assign Net debt
def select_debt(row):
    year = row['IPO date'].year
    debt_column = f"Net debt\nth EUR {year}"
    return row.get(debt_column, pd.NA)

df['Net debt (th)'] = df.apply(select_debt, axis=1)

# Assign Cash
def select_cash(row):
    year = row['IPO date'].year
    cash_column = f"Cash and cash equivalent\nth EUR {year}"
    return row.get(cash_column, pd.NA)

df['Cash & cash equivalent (th)'] = df.apply(select_cash, axis=1)

# Calculate total debt / total assets
df['Total assets (th)'] = df['Total assets (th)'].str.replace(',', '')
df['Total assets (th)'] = pd.to_numeric(df['Total assets (th)'], errors='coerce')
df['Net debt (th)'] = df['Net debt (th)'].str.replace(',', '')
df['Net debt (th)'] = pd.to_numeric(df['Net debt (th)'], errors='coerce')
df['Cash & cash equivalent (th)'] = df['Cash & cash equivalent (th)'].str.replace(',', '')
df['Cash & cash equivalent (th)'] = pd.to_numeric(df['Cash & cash equivalent (th)'], errors='coerce')

df['Total debt (th)']=df['Net debt (th)']+df['Cash & cash equivalent (th)']
df['Total debt / Total assets']=df['Total debt (th)']/df['Total assets (th)']

# Remove helper columns
columns_to_drop_debt_cash=['Net debt\nth EUR 2023',
                             'Net debt\nth EUR 2022',
                             'Net debt\nth EUR 2021',
                             'Net debt\nth EUR 2020',
                             'Cash and cash equivalent\nth EUR 2023',
                             'Cash and cash equivalent\nth EUR 2022',
                             'Cash and cash equivalent\nth EUR 2021',
                             'Cash and cash equivalent\nth EUR 2020']

df.drop(columns=columns_to_drop_debt_cash, inplace=True)

# Convert Sales columns to numeric and remove commas
years = ['2023', '2022', '2021', '2020', '2019']

for year in years:
    column_name = f'Sales\nth EUR {year}'
    df[column_name] = df[column_name].str.replace(',', '')
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    
# Assign Sales from the previous year
def select_sales(row):
    year = row['IPO date'].year-1
    sales_column = f"Sales\nth EUR {year}"
    return row.get(sales_column, pd.NA)

df['Sales (th)'] = df.apply(select_sales, axis=1)

# Remove helper columns
df = df.drop('Sales\nth EUR 2023', axis=1)
df = df.drop('Sales\nth EUR 2022', axis=1)
df = df.drop('Sales\nth EUR 2021', axis=1)
df = df.drop('Sales\nth EUR 2020', axis=1)
df = df.drop('Sales\nth EUR 2019', axis=1)

# Export to csv file
df.to_csv(r'C:\Users\arnel\OneDrive - KU Leuven\Thesis Economics\Python\Data\prepared data 2.csv', index=False)
df.to_csv(r'C:\Users\arnel\thesis\CSV FILES\prepared data 2.csv', index=False)
print('prepared data 2 = ready')
