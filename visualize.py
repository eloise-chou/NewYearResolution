import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
import cv2 as cv
import numpy as np
import shapely
from model.get_polygon import get_polygon
from shapely import affinity

# data
MRT_sum_with_coord = pd.read_csv('./DATA/MRT_sum_with_coord_contain_22-05.csv')

st.title("捷運站跨年人潮熱點圖")
st.subheader("前言")
st.text("2024 年首度來到台北 101 跨年，著實被一級戰區的人潮嚇到，活動結束跟著散場的人潮慢慢移動到最近的台北\n捷運 101 站後，發現進站人潮已經大排長龍，因此決定前往與其相鄰的捷運象山站，但當抵達後發現捷運象山站\n的排隊人潮與捷運 101 站的人潮相彷，多走了一段冤枉路讓我不禁好奇到底前往哪一個捷運站可以最快進站。")
st.subheader("政府應對措施")
st.text("為了有效率的疏散跨年人潮，台北市政府實施了以下措施：")
st.text("1. 台北捷運連續 42 小時營運\n2. 調整捷運班距時間\n3. 規劃 3 線散場接駁車至捷運忠孝新生、公館、景美以及木柵")
st.subheader("資料蒐集")
st.text("我利用政府資料開放平台提供的「臺北捷運各站分時進出量統計」再結合台北捷運位置資料，")

selected_year = st.selectbox("請選擇年份:", list(range(2018, 2024)))

MRT_sum_with_coord_select_year = MRT_sum_with_coord[MRT_sum_with_coord['year'] == selected_year]

#read the image
img = cv.imread("./DATA/tp101.jpg")
#convert the image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#Apply thresholding to the image
ret, thresh = cv.threshold(gray, 200, 255, cv.THRESH_OTSU)
#find the contours in the image
contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#draw the obtained contour lines(or the set of coordinates forming a line) on the original image
cv.drawContours(img, contours,1, (0,255,0), 5)
#show the image

SCALE = 100_000

## Translation
contour_101_polygon = shapely.Polygon(contours[1].reshape(-1,2))
rotated = affinity.rotate(contour_101_polygon, 180, 'center')  
mapped_coord  = shapely.geometry.mapping(rotated)['coordinates'][0]

lons = [c[0]/SCALE + 121.562427 for c in mapped_coord]
lats = [c[1]/SCALE + 25.032071 for c in mapped_coord]

mylayers =[get_polygon(lons=lons, lats=lats,  color='gray')]

fig = px.density_mapbox(MRT_sum_with_coord_select_year, lat='緯度', lon='經度', z='人次', radius=60, zoom=12,
                        center=dict(lat=25.033671, lon=121.564427),
                        mapbox_style="carto-positron", animation_frame="時段", 
                        category_orders= {"時段": [22, 23, 0, 1, 2, 3, 4, 5]}, 
                        hover_name="exit", color_continuous_scale='Reds', range_color=[500,1500])
fig.layout.update(mapbox_layers = mylayers)
fig.update_layout(
    autosize=False,
    width=800,
    height=600,
)

st.plotly_chart(fig, use_container_width=True)