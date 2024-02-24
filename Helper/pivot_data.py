import pandas as pd

def pivot(file):
    df = pd.read_excel(file)

    # Melt the DataFrame to convert days into rows
    df = pd.melt(df, id_vars=['Tribal Member'], var_name='Day', value_name='Pushups')

    # Convert 'Day' to datetime type with a specific format
    df['Day'] = pd.to_datetime(df['Day'])
    df['Month'] = df['Day'].dt.month_name()
    df['Week'] = (df['Day'] - pd.to_timedelta(df['Day'].dt.dayofweek, unit='D')).dt.strftime('%m/%d to ') + (df['Day'] + pd.to_timedelta(6 - df['Day'].dt.dayofweek, unit='D')).dt.strftime('%m/%d')

    # Define a custom aggregation function for sum/count
    def avg_pushup_perc(x):
        return x.sum() / x.count() if x.count() > 0 else 0

    # 
    grouped_df = df.groupby('Tribal Member').agg({'Pushups': avg_pushup_perc})
    grouped_df = grouped_df.reset_index()
    grouped_df['Tribal Member'] = grouped_df['Tribal Member'].astype('object')


    # Apply the cumulative sum within each group of 'Tribal Member'
    df['Cumulative_Pushups'] = df.groupby('Tribal Member')['Pushups'].cumsum()
    df['Cumulative_Days'] = df.groupby('Tribal Member').cumcount() + 1
    df['Cumulative_Percentage'] = df['Cumulative_Pushups'] / df['Cumulative_Days']


    # Pivot the table
    cumulative_pivot_table = pd.pivot_table(df, values='Cumulative_Percentage', index='Tribal Member', columns='Day', fill_value=0)
    cumulative_pivot_table.columns = [f'{col.strftime("%m/%d")}' for col in cumulative_pivot_table.columns]
    cumulative_pivot_table = cumulative_pivot_table.reset_index()
    cumulative_pivot_table['Tribal Member'] = cumulative_pivot_table['Tribal Member'].astype('object')


    # Pivot the table
    month_pivot_table = pd.pivot_table(df, values='Pushups', index='Tribal Member', columns='Month',
                                aggfunc={'Pushups': [avg_pushup_perc]}, fill_value=0).reset_index()
    month_pivot_table.columns = ['Tribal Member'] + [f'{col[1]}' for col in month_pivot_table.columns[1:]]


    # Pivot the table
    week_pivot_table = pd.pivot_table(df, values='Pushups', index='Tribal Member', columns='Week',
                                aggfunc={'Pushups': [avg_pushup_perc]}, fill_value=0).reset_index()
    week_pivot_table.columns = ['Tribal Member'] + [f'{col[1]}' for col in week_pivot_table.columns[1:]]



    # Merge the DataFrames
    result_df = pd.merge(grouped_df, month_pivot_table, on='Tribal Member', how='left')
    visual_df = pd.merge(result_df, week_pivot_table, on='Tribal Member', how='left')

    # Function to convert columns to percentage with 0 decimal places
    def convert_to_percent(x):
        return "{:.0%}".format(x)

    visual_df.iloc[:, 1:] = visual_df.iloc[:, 1:].applymap(convert_to_percent)
    cumulative_pivot_table.iloc[:, 1:] = cumulative_pivot_table.iloc[:, 1:].applymap(convert_to_percent)

    cumulative_pivot_table = pd.melt(cumulative_pivot_table, id_vars=['Tribal Member'], var_name='Day', value_name='Cumulative Perc')

    return visual_df, cumulative_pivot_table

    # # Create an Excel writer object
    # excel_writer = pd.ExcelWriter('pivoted_data.xlsx', engine='xlsxwriter')

    # # Write each DataFrame to a different Excel sheet
    # visual_df.to_excel(excel_writer, sheet_name='result_df', index=False)
    # cumulative_pivot_table.to_excel(excel_writer, sheet_name='cumulative_pivot_table', index=False)

    # # Save the Excel file
    # excel_writer.save()

agg1, cumm1 = pivot("TTK_Pushups.xlsx")