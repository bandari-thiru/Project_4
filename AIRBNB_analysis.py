import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis by Sudhakar Bandari!!!", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart:   AirBnb-Analysis")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# with st.headbar:
SELECT = option_menu(
    menu_title=None,
    options=["Home", "Explore Data", "Tableau Dashboard"],
    icons=["house", "bar-chart", "list-task"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "black", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
            "nav-link-selected": {"background-color": "#6F36AD"}})

#----------------Home----------------------#

if SELECT == "Home":

 st.header('Airbnb Analysis')
 st.subheader("Airbnb is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. The company is credited with revolutionizing the tourism industry, while also having been the subject of intense criticism by residents of tourism hotspot cities like Barcelona and Venice for enabling an unaffordable increase in home rents, and for a lack of regulation.")
 st.subheader('Skills take away From This Project:')
 st.subheader('Python Scripting, Data Preprocessing, Visualization, EDA, Streamlit, MongoDB, Tableau')
 st.subheader('Domain:')
 st.subheader('Travel Industry, Property management and Tourism')

if SELECT == "Explore Data":
 fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
 if fl is not None:
    filename = fl.name
    st.write(filename)
    #df = pd.read_csv(filename, encoding="ISO-8859-1")
    df = pd.read_csv(filename, encoding="ISO-8859-1")
 else:
    os.chdir("C:/Users/Admin/Documents/Project_4")
    df = pd.read_csv("airbnb.csv", encoding="ISO-8859-1")

 st.sidebar.header("Choose your filter: ")

 # Create for neighbourhood_group
 host_neighbourhood = st.sidebar.multiselect("Pick your host_neighbourhood", df["host_neighbourhood"].unique())
 if not host_neighbourhood:
     df2 = df.copy()
 else:
     df2 = df[df["host_neighbourhood"].isin(host_neighbourhood)]

 # Create for neighbourhood
 host_name = st.sidebar.multiselect("Pick the host_neighbourhood", df2["host_neighbourhood"].unique())
 if not host_name:
     df3 = df2.copy()
 else:
     df3 = df2[df2["host_neighbourhood"].isin(host_name)]

 # Filter the data based on neighbourhood_group, neighbourhood

 if not host_neighbourhood and not host_name:
     filtered_df = df
 elif not host_name:
     filtered_df = df[df["host_neighbourhood"].isin(host_neighbourhood)]
 elif not host_neighbourhood:
     filtered_df = df[df["host_neighbourhood"].isin(host_name)]
 elif host_name:
     filtered_df = df3[df["host_neighbourhood"].isin(host_name)]
 elif host_neighbourhood:
     filtered_df = df3[df["host_neighbourhood"].isin(host_neighbourhood)]
 elif host_neighbourhood and host_name:
     filtered_df = df3[df["host_neighbourhood"].isin(host_neighbourhood) & df3["host_name"].isin(host_name)]
 else:
     filtered_df = df3[df3["host_neighbourhood"].isin(host_neighbourhood) & df3["host_name"].isin(host_name)]

 room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

 col1, col2 = st.columns(2)
 with col1:
    st.subheader("room_type_ViewData")
    fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

 with col2:
    st.subheader("neighbourhood_group_ViewData")
    fig = px.pie(filtered_df, values="price", names="host_neighbourhood", hole=0.5)
    fig.update_traces(text=filtered_df["host_neighbourhood"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

 cl1, cl2 = st.columns((2))
 with cl1:
    with st.expander("room_type wise price"):
        st.write(room_type_df.style.background_gradient(cmap="Blues"))
        csv = room_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 with cl2:
    with st.expander("host_neighbourhood wise price"):
        neighbourhood_group = filtered_df.groupby(by="host_neighbourhood", as_index=False)["price"].sum()
        st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
        csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="host_neighbourhood.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 # Create a scatter plot
 data1 = px.scatter(filtered_df, x="host_neighbourhood", y="host_name", color="room_type")
 data1['layout'].update(title="Room_type in the host_name and host_neighbourhood wise data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="Neighbourhood_Group", titlefont=dict(size=20)),
                        yaxis=dict(title="Neighbourhood", titlefont=dict(size=20)))
 st.plotly_chart(data1, use_container_width=True)

 with st.expander("Detailed Room Availability and Price View Data in the host_name"):
     st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

 # Download orginal DataSet
 csv = df.to_csv(index=False).encode('utf-8')
 st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

 import plotly.figure_factory as ff

 st.subheader(":point_right: host_neighbourhood wise Room_type and Minimum stay nights")
 with st.expander("Summary_Table"):
    df_sample = df[0:5][["host_neighbourhood", "host_name", "review_scores", "room_type", "price", "minimum_nights", "host_name"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

 # map function for room_type

# If your DataFrame has columns 'Latitude' and 'Longitude':
 st.subheader("Airbnb Analysis in Map view")
 df = df.rename(columns={"Latitude": "lat", "Longitude": "lon"})

 st.map(df)

# ----------------------Contact---------------#

if SELECT == "Tableau Dashboard":
    image = 'tableau dashboard 2.PNG'
    st.image(image, use_column_width=True)

    
if SELECT == "Contact":
    Name = (f'{"Name :"}  {"SUDHAKAR BANDARI"}')
    mail = (f'{"Mail :"}  {"bandari.sudhakar@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {"GITHUB": "https://github.com/bandari-thiru/Project_4"}
        
    col1, col2 = st.columns(2)
    col1.image(Image.open("C:/Users/Admin/Documents/Project_4/Sudhakar_Image.jpeg"), width=300)
                          
    with col2:
        st.header('Airbnb Analysis')
        st.subheader(
            "This project aims to analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive geospatial visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
        st.write("---")
        st.subheader(Name)
        st.subheader(mail)

    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")