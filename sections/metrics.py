import streamlit as st
import pandas as pd

def show_metrics_quality(df,COLORS):
    
    st.title("Dataset Overview & Metrics")

    st.markdown(
        f"""
        <div style="color:{COLORS['text']};">
        This page provides <strong>key metrics</strong> for the video games dataset and a quick overview of its <strong>data quality</strong>.
        It helps understand the dataset before diving into detailed analyses.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metrics Header (KPIs) 
    st.subheader("Key Metrics (KPIs)")

    total_games = len(df)
    total_reliable = df['has_reliable_votes'].sum()
    average_rating = round(df['total_rating'].mean(), 2)
    average_rating_reliable = round(df[df['has_reliable_votes']]['total_rating'].mean(), 2)
    first_year = df['first_release_date'].dt.year.min()
    last_year = df['first_release_date'].dt.year.max()

    # Display KPIs in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Games", total_games)
    col2.metric("Games with Reliable Votes", total_reliable)
    col3.metric("Average Rating", average_rating)

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Reliable Rating", average_rating_reliable)
    col2.metric("First Release Year", first_year)
    col3.metric("Last Release Year", last_year)

    st.markdown("---")

    # Data Quality Section 
    st.subheader("Data Quality Checks")

    # Missing values
    missing_df = df.isna().sum().reset_index()
    missing_df.columns = ["Column", "Missing Values"]
    missing_df["Percentage"] = (missing_df["Missing Values"] / len(df) * 100).round(2)

    st.markdown(f"<h5 style='color:{COLORS['highlight']}'>Missing Values by column</h5>", unsafe_allow_html=True)
    st.dataframe(missing_df, use_container_width=True)

    # Duplicates
    st.markdown(f"<span style='color:{COLORS['subtext']}'>Number of duplicate rows: {df.duplicated().sum()}</span>", unsafe_allow_html=True)

    # Validation checks
    st.markdown("<h3 style='color:{}'>Validation Checks</h3>".format(COLORS['highlight']), unsafe_allow_html=True)

    invalid_ratings = df[(df['total_rating'] < 0) | (df['total_rating'] > 100)].shape[0]
    st.markdown(f"- Games with invalid ratings (<0 or >100): <span style='color:{COLORS['negative']}'>{invalid_ratings}</span>", unsafe_allow_html=True)

    valid_age_ratings = ["Everyone", "Child", "Teen", "Young", "18+"]
    invalid_age = df[df["age_rattings"].apply(lambda x: x not in valid_age_ratings)].shape[0]
    st.markdown(f"- Games with invalid age rating: <span style='color:{COLORS['negative']}'>{invalid_age}</span>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="color:{COLORS['subtext']};">
        _These checks help ensure that the dataset is <strong>reliable</strong> for analysis._
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Column Descriptions
    st.subheader("Dataset Columns Explanation")
    st.markdown(
        f"""
        <div style="color:{COLORS['text']}">
        
        - **name** - Name of the game  
        - **first_release_date** - Date when the game was first released  
        - **cover** - Cover image of the game  
        - **total_rating** - Average score combining player and journalist ratings  
        - **has_reliable_votes** - Indicates if the ratings are considered reliable  

        - **developer_company** - Company that developed the game  
        - **developer_country** - Country of the developer company  
        - **publisher_company** - Company that published the game  
        - **publisher_country** - Country of the publisher company  

        - **platforms** - Specific platforms where the game is available (PC, PS5, Switch, etc.)  
        - **platform_family** - Group of similar platforms (e.g., PlayStation, Xbox, Nintendo)  
        - **platform_type** - Type of platform (console, handheld, etc.)  
        - **generation_platform** - Generation of the platform (e.g., 6, 7)  

        - **age_rattings** - Age rating of the game (e.g., Everyone, Teen, 18+)  

        - **game_type** - Type or category of the game (e.g., single-player, multiplayer)  
        - **game_modes** - Available modes (e.g., co-op, online, local multiplayer)  
        - **player_perspectives** - Perspective from which the game is played (e.g., first-person, third-person)  
        - **genres** - Genres of the game (e.g., action, RPG, indie)  

        - **collections** - Indicates if the game is part of a license or franchise  
        - **remake** - Indicates if the game has a remake  
        - **remaster** - Indicates if the game has a remaster  
        - **early_access** - Indicates if the game was released in early access  
        - **dlcs** - Number of DLCs available for the game  
        </div>
        """,
        unsafe_allow_html=True
    )
