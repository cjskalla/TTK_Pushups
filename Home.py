import streamlit as st
import pandas as pd
import plotly.express as px
from Helper import pivot_data as pv
import numpy as np

#Title
title = st.markdown(
        f"""
        <h3 style="
            text-align: center;
            font-family: Forum;
            font-weight: 100;
            font-size: 300%;
            ">
            TESTING
        </h1>
        """,
        unsafe_allow_html=True
    )


inputs = pd.read_excel("inputs.xlsx")

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(inputs)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)

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

agg1, df_cumm1 = pv.pivot()

cumm1 = df_cumm1.drop_duplicates(subset=["Tribal Member", "Day"])

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
            "Trend", y_min=0, y_max=1
        )
    },
    height=425,
    hide_index=True,
    use_container_width=True
)


# Define a dictionary with Tribal Members and their corresponding hex code colors
tribal_member_colors = {
    'Bino':             '#B03060', # (Redish)         
    'Calvin':           '#ffffff', # (White)          
    'Carter':           '#ff0000', # (Red)            
    'Charlie':          '#00ff00', # (Green)          
    'David':            '#0000ff', # (Blue)           
    'Kade':             '#ffff00', # (Yellow)         
    'Parker':           '#ff00ff', # (Magenta)        
    'Petey':            '#00ffff', # (Cyan)           
    'Ryan':             '#ff9900', # (Orange)         
    'Tauke':            '#9900ff', # (Purple)         
    'Von':              '#00cc00'  # (Dark Green)
}


cumm1["Cumulative Perc"] = cumm1["Cumulative Perc"] * 100

# Add jitter to the x-axis values
cumm1['Jittered Perc'] = cumm1['Cumulative Perc'] + np.random.normal(0, 5, len(cumm1))

# Create the line chart with Plotly Express
fig = px.line(cumm1, x='Jittered Perc', y='Day', color='Tribal Member', line_group='Tribal Member',
              labels={'Jittered Perc': 'Cumulative Perc', 'Day': 'Day'})


# Customize the layout including the height
fig.update_layout(title='All Time %',
                  title_x=0.4,  # Center the title
                  title_y=0.92,
                  xaxis_title='',
                  yaxis_title='',
                  height=600,
                  width=350,
                  xaxis=dict(range=[-15, 115], tickvals=[0, 25, 50, 75, 100], ticktext=['0%', '25%', '50%', '75%', '100%']),
                  legend_title_text='', 
                  legend_itemsizing='constant',
                  legend_font_size=15,
                  legend=dict(y=-.07, orientation='h')
)


# Update traces with custom colors
for member, color in tribal_member_colors.items():
    fig.update_traces(selector={'name': member}, line=dict(color=color))



st.plotly_chart(fig, use_container_width=True)