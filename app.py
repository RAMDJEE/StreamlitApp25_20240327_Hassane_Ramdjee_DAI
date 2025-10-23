# Import the required libraries
import streamlit as st
import pandas as pd
from utils.io import load_data
import pathlib

# Import the various pages
from sections.home import show_home 
from sections.notes import show_notes 
from sections.metrics import show_metrics_quality
from sections.quantity import show_quantity
from sections.Map import show_map
from sections.conclusion import show_conclusion


# Function to load CSS from the "assets" folder
def load_css(file_path):
    with open(file_path) as f:
        st.html(f"<style>{f.read()}</style>")
# Load the external CSS
css_path = pathlib.Path("assets/intro.css")
load_css(css_path)

# Config page 
st.set_page_config(
    page_title="21st Century Gaming",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="auto",
)

# Load data
@st.cache_data
def get_data():
    df = load_data()
    return df
df = load_data()

# The right data types
df["name"] = df["name"].astype("string")
df["first_release_date"] = df["first_release_date"].astype("datetime64[ns]")
df["cover"] = df["cover"].astype("string")
df["total_rating"] = df["total_rating"].astype("float64")
df["developer_company"] = df["developer_company"].astype("object")
df["developer_country"] = df["developer_country"].astype("object")
df["publisher_company"] = df["publisher_company"].astype("object")
df["publisher_country"] = df["publisher_country"].astype("object")
df["platforms"] = df["platforms"].astype("object")
df["platform_family"] = df["platform_family"].astype("object")
df["platform_type"] = df["platform_type"].astype("category")
df["generation_platform"] = df["generation_platform"].astype("Int64")
df["game_type"] = df["game_type"].astype("category")
df["game_modes"] = df["game_modes"].astype("object")
df["player_perspectives"] = df["player_perspectives"].astype("object")
df["genres"] = df["genres"].astype("object")
df["remake"] = df["remake"].astype("bool")
df["remaster"] = df["remaster"].astype("bool")
df["early_access"] = df["early_access"].astype("bool")
df["dlcs"] = df["dlcs"].astype("int64")
df["generation_platform"] = df["generation_platform"].astype("int64")
df["age_rattings"] = df["age_rattings"].astype("category")
df["has_reliable_votes"] = df["has_reliable_votes"].astype("bool")



## Navigation part

# Sidebar title
st.sidebar.markdown(
    """
    <div style="
        font-size: 28px;
        font-weight: bold;
        color: #4e79a7;
        text-align: center;
        padding: 10px 0;
    ">
        Navigation
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize page in session state
if "page" not in st.session_state:
    st.session_state.page = "Home"
    
# Sidebar buttons
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Metrics & Quality"):
    st.session_state.page = "Metrics"
if st.sidebar.button("Game Quality - Ratings"):
    st.session_state.page = "Ratings"
if st.sidebar.button("Game Quantity - Releases"):
    st.session_state.page = "Quantity"
if st.sidebar.button("Developer and Publisher"):
    st.session_state.page = "Map"
if st.sidebar.button("Conclusion"):
    st.session_state.page = "Conclusion"

# Display page based on selection
if st.session_state.page == "Home":
    show_home(df)
elif st.session_state.page == "Metrics":
    show_metrics_quality(df)
elif st.session_state.page == "Ratings":
    show_notes(df) 
elif st.session_state.page == "Quantity":
    show_quantity(df)
elif st.session_state.page == "Map":
    show_map(df)
elif st.session_state.page == "Conclusion":
    show_conclusion(df)