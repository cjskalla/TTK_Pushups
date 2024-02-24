import streamlit as st
import pandas as pd
from Helper import pivot_data as pv


col = st.columns([1,2,1])

with col[1]:
    st.title("TTK Tribal Rankings")

agg1, cumm1 = pv.pivot("TTK_Pushups.xlsx")



st.dataframe(agg1)

st.divider()

st.line_chart(cumm1, )
