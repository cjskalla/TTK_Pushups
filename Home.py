import streamlit as st
import pandas as pd
import random
from Helper import pivot_data as pv


col = st.columns([1,2,1])

with col[1]:
    st.title("TTK Tribal Rankings")

agg1, cumm1 = pv.pivot("TTK_Pushups.xlsx")


# Pivot the DataFrame
pivot_cumm1 = cumm1.pivot(index='Tribal Member', columns='Day', values='Cumulative Perc')
pivot_cumm1.reset_index(inplace=True)


merged_df = pd.merge(agg1, pivot_cumm1, on='Tribal Member', how='left')

# Create Cumulative Score column with reordered values
merged_df['Cumulative Score'] = merged_df.apply(lambda row: row[pivot_cumm1.columns[1:]].dropna().tolist(), axis=1)
merged_df.drop(columns=pivot_cumm1.columns[1:], inplace=True)


merged_df["Pushups"] = merged_df["Pushups"] * 100

st.dataframe(
    merged_df.loc[:, ["Tribal Member", "Pushups", "Cumulative Score"]],
    column_config={
        "Tribal Member": "Tribal Member",
        "Pushups": st.column_config.ProgressColumn(
            "%",
            help="All Time Pushup Consistency %",
            format="%d %%",
            min_value=0,
            max_value=100
        ),
        "Cumulative Score": st.column_config.LineChartColumn(
            "History", y_min=0, y_max=1
        )
    },
    height=425,
    hide_index=True,
    use_container_width=True
)


st.divider()

merged_df
cumm1

# st.line_chart(cumm1)
