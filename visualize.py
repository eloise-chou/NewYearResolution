import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px

# data
MRT_sum_with_coord = pd.read_csv('./DATA/MRT_sum_with_coord.csv')

st.header("捷運站跨年人潮熱點圖")

selected_year = st.selectbox("請選擇年份:", list(range(2018, 2024)))

MRT_sum_with_coord_select_year = MRT_sum_with_coord[MRT_sum_with_coord['year'] == selected_year]

fig = px.density_mapbox(MRT_sum_with_coord_select_year, lat='緯度', lon='經度', z='人次', radius=50, zoom=12.5,
                        center=dict(lat=25.033671, lon=121.564427),
                        mapbox_style="carto-positron", animation_frame="時段", hover_name="exit",
                        color_continuous_scale='Reds')

st.plotly_chart(fig, use_container_width=True)