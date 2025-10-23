import streamlit as st
import pandas as pd

def show_metrics_quality(df):
    st.title("Dataset Overview & Metrics")
    st.markdown(
        """
        This page provides **key metrics** for the video games dataset and a quick overview of its **data quality**.
        It helps understand the dataset before diving into detailed analyses.
        """
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

    st.markdown("##### Missing Values by column")
    st.dataframe(missing_df, use_container_width=True)

    # Duplicates
    st.markdown(f"**Number of duplicate rows:** {df.duplicated().sum()}")


    # Validation checks
    st.markdown("### Validation Checks")

    invalid_ratings = df[(df['total_rating'] < 0) | (df['total_rating'] > 100)].shape[0]
    st.markdown(f"- Games with invalid ratings (<0 or >100): {invalid_ratings}")

    valid_age_ratings = ["Everyone", "Child", "Teen", "Young", "18+"]
    invalid_age = df[df["age_rattings"].apply(lambda x: x not in valid_age_ratings)].shape[0]
    st.markdown(f"- Games with invalid age rating: {invalid_age}")

    st.markdown(
        """
        _These checks help ensure that the dataset is **reliable** for analysis._  
        """
    )