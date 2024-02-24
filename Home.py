import streamlit as st
import pandas as pd
import plotly.express as px
from Helper import pivot_data as pv


#Title
title = st.markdown(
        f"""
        <h3 style="
            text-align: center;
            font-family: Forum;
            font-weight: 100;
            font-size: 300%;
            ">
            TTK Tribal Rankings
        </h1>
        """,
        unsafe_allow_html=True
    )

agg1, cumm1 = pv.pivot("TTK_Pushups.xlsx")


# Pivot the DataFrame
pivot_cumm1 = cumm1.pivot(index='Tribal Member', columns='Day', values='Cumulative Perc')
pivot_cumm1.reset_index(inplace=True)


merged_df = pd.merge(agg1, pivot_cumm1, on='Tribal Member', how='left')

# Create Cumulative Score column with reordered values
merged_df['Cumulative Score'] = merged_df.apply(lambda row: row[pivot_cumm1.columns[1:]].dropna().tolist(), axis=1)
merged_df.drop(columns=pivot_cumm1.columns[1:], inplace=True)
merged_df["Pushups"] = merged_df["Pushups"] * 100
merged_df_sorted = merged_df.sort_values(by="Pushups", ascending=False)



st.dataframe(
    merged_df_sorted.loc[:, ["Tribal Member", "Pushups", "Cumulative Score"]],
    column_config={
        "Tribal Member": "Tribal Member",
        "Pushups": st.column_config.ProgressColumn(
            "%",
            help="All Time Pushup Consistency %",
            format="%d %%",
            width='small',
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


cumm1["Cumulative Perc"] = cumm1["Cumulative Perc"] * 100

# Create the line chart with Plotly Express
fig = px.line(cumm1, x='Cumulative Perc', y='Day', color='Tribal Member', line_group='Tribal Member',
              labels={'Cumulative Perc': 'Cumulative Perc', 'Day': 'Day'})

# Customize the layout including the height
fig.update_layout(title='All Time %',
                  title_x=0.4,  # Center the title
                  xaxis_title='',
                  yaxis_title='',
                  height=800,
                  width=350,
                  xaxis=dict(range=[0, 100], tickvals=[0, 25, 50, 75, 100], ticktext=['0%', '25%', '50%', '75%', '100%']),
                  legend_title_text='', 
                  legend_itemsizing='constant',
                  legend_font_size=15,  # Set legend font size
                  legend=dict(y=-.05, orientation='h') 
)


st.plotly_chart(fig, use_container_width=True)