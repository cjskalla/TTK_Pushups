import streamlit as st
import pandas as pd


df = pd.read_excel("TTK_Pushups.xlsx")

# Melt the DataFrame to convert days into rows
df = pd.melt(df, id_vars=['Tribal Member'], var_name='Day', value_name='Pushups')

# Convert 'Day' to datetime type with a specific format
df['Day'] = pd.to_datetime(df['Day'])

# Extract month from the 'Day' column
df['Month'] = df['Day'].dt.month_name()

# Extract month from the 'Day' column
df['Week'] = df['Day'].dt.strftime('%m/%d - ') + (df['Day'] + pd.DateOffset(days=6)).dt.strftime('%m/%d')




# Define a custom aggregation function for sum/count
def avg_pivot(x):
    return x.sum() / x.count() if x.count() > 0 else 0

# Pivot the table
total_pivot_table = df.groupby('Tribal Member')['Pushups']

# Pivot the table
month_pivot_table = pd.pivot_table(df, values='Pushups', index='Tribal Member', columns='Month',
                             aggfunc={'Pushups': ['count', 'sum', avg_pivot]}, fill_value=0).reset_index()

# Rename columns for better readability
month_pivot_table.columns = [f'{col[0]}_{col[1]}' for col in month_pivot_table.columns]


# Pivot the table
week_pivot_table = pd.pivot_table(df, values='Pushups', index='Tribal Member', columns='Week',
                             aggfunc={'Pushups': ['count', 'sum', avg_pivot]}, fill_value=0).reset_index()


# Rename columns for better readability
week_pivot_table.columns = [f'{col[0]}_{col[1]}' for col in week_pivot_table.columns]