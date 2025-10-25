# Import the required libraries
import streamlit as st
import pandas as pd
import numpy as np
import ast

# Import the various functions
from utils.visualisation_quantity import plot_general
from utils.visualisation_quantity import plot_by_indie
from utils.visualisation_quantity import camemberg_genres
from utils.visualisation_quantity import parallele_comp


def show_quantity(df,COLORS):
    
    # Title and introduction 
    st.title("Number of Release")

    st.markdown(
        """
        The quantity of video games released is closely linked to the notion of quality: the more games there are, the greater the potential impact on average ratings.
        Beyond this, examining quantity allows us to highlight trends in specific sectors, sudden bursts of popularity, and the emergence of new markets or countries in game production. 
        In short, quantity carries a lot of information and brings a fresh perspective to our analysis.

        **Note:** 
        - When collecting the data, we deliberately excluded fan games, cancelled projects, and ports. 
        This affects the total number of releases, especially since some studios focus entirely on these types of projects, 
        which may create gaps in the dataset despite their work.
        - Regarding ports, only official remakes and remasters are included. 
        Definitive editions, simple PC versions, or other minor ports are not counted.
        """
    )

    st.markdown(
        """
        Here, we will explore the number of games released per platform, the surge of indie titles, and other interesting trends.  
        """
    )

    st.markdown(
        f"""
        Before anything else, it is important to examine the number of games released each year, as this will serve as our baseline.  
        Initially, we considered **all the games in our database** to see how many were released per year (represented by the green graph). However, a major issue immediately arose: why was there such a huge spike around 2017? The data was clearly inconsistent.  

        To address this, we then focused **only on games with 100% internationally recognized ratings**, i.e., those with reliable votes. This produced a more coherent graph (shown in red), although the spike between 2015 and 2018 still persisted, albeit less pronounced.
        This red graph represents our **primary working dataset**: it is the most reliable and consistent source we have.  

        Nevertheless, it was still interesting to compare with **the true values from IGDB**, the source of our database. This time, we collected **all games**, still applying the filter by game type (excluding ports and DLCs), but removing the rating filter: so even unrated games were included. This resulted in the blue graph, which shows a clear, continuous increase in releases over time.  

        It is important to note that our red graph is **not incorrect**: it simply reflects that journalists and critics review far fewer games, with a peak in ratings around 2015–2018. Unfortunately, we cannot control this phenomenon.  

        Moving forward, instead of relying on raw release numbers, we will focus on **percentages of a category relative to the total releases per year**. This approach reduces the impact of such biases and allows for a more accurate comparison across years.  

        <p style="font-style: italic; color: {COLORS['subtext']}; margin-top: 10px;">
        Note: You can hover over the graphs to see the exact numbers, as these are interactive plots with hover functionality.
        </p>
        """,
        unsafe_allow_html=True
    )

    df["first_release_date"] = df["first_release_date"].dt.year

    df_general = df.groupby(["first_release_date", "has_reliable_votes"]).size().reset_index(name="number_of_games")
    df_general = df_general[df_general["has_reliable_votes"] == True]

    fig = plot_general(df_general, COLORS["negative"], "Number of games released per year (with reliable vote)")
    st.plotly_chart(fig)

    col1, col2 = st.columns([1,1])

    with col1:
        df_general_novote = df.groupby("first_release_date").size().reset_index(name="number_of_games")
        fig = plot_general(df_general_novote, COLORS["positive"], "Number of games released per year (with rating, reliable or not)")
        st.plotly_chart(fig)

    with col2:
        years = list(range(2000, 2026))
        totals = [1563, 1610, 1639, 1578, 1533, 1752, 1908, 2196, 2437, 2906,3021, 2968, 3090, 3286, 4282, 5517, 7626, 10303, 10961, 10259,11511, 13822, 13725, 16778, 20718, 16832]
        df_all_games = pd.DataFrame({"first_release_date": years,"number_of_games": totals})
        df_all_games["all_games"] = True
        fig = plot_general(df_all_games, COLORS["highlight"], "Number of games released per year")
        st.plotly_chart(fig)

    st.markdown("---")


    col3, col4 = st.columns([1,1])
    with col3:
        df_rating_genres = df[["first_release_date", "total_rating", "has_reliable_votes", "genres"]]
        df_rating_genres = df_rating_genres[df_rating_genres["has_reliable_votes"] == True]

        df_rating_genres["genres"] = df_rating_genres["genres"].apply(lambda x: ast.literal_eval(x))
        df_rating_genres["is_indie"] = df_rating_genres["genres"].apply(lambda x: "Indie" in x if isinstance(x, list) else False)
        df_rating_genres = df_rating_genres.groupby(["first_release_date", "has_reliable_votes", "is_indie"]).size().reset_index(name="number_of_games_indie")

        df_rating_genres = df_rating_genres.merge(df_general[["first_release_date", "number_of_games"]],on="first_release_date",how="left")
        df_rating_genres["number_of_games_indie"] = (df_rating_genres["number_of_games_indie"] * 100) / df_rating_genres["number_of_games"]
        
        fig = plot_by_indie(df_rating_genres, "Number of Indie games released per year in percentage (with reliable vote)")
        st.plotly_chart(fig)
    
    with col4: 
        df_rating_genres_novote = df[["first_release_date", "total_rating", "has_reliable_votes", "genres"]]

        df_rating_genres_novote["genres"] = df_rating_genres_novote["genres"].apply(lambda x: ast.literal_eval(x))
        df_rating_genres_novote["is_indie"] = df_rating_genres_novote["genres"].apply(lambda x: "Indie" in x if isinstance(x, list) else False)
        df_rating_genres_novote = df_rating_genres_novote.groupby(["first_release_date", "has_reliable_votes", "is_indie"]).size().reset_index(name="number_of_games_indie")

        df_rating_genres_novote = df_rating_genres_novote.merge(df_general_novote[["first_release_date", "number_of_games"]],on="first_release_date",how="left")
        df_rating_genres_novote["number_of_games_indie"] = (df_rating_genres_novote["number_of_games_indie"] * 100) / df_rating_genres_novote["number_of_games"]
        
        fig = plot_by_indie(df_rating_genres_novote, "Number of Indie games released per year in percentage (with rating, reliable or not)")
        st.plotly_chart(fig)

    st.markdown(
        f"""
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: {COLORS['highlight']}; margin-bottom: 15px;">
                The Rise of Indie Games Over Time
            </p>
            <p style="color:{COLORS['text']}">
                In these graphs, we observe the <b>percentage of indie games</b> released each year 
                compared to the total number of games published. 
                Whether we include only titles with reliable votes or all available data, 
                the conclusion remains the same: <b>the indie sector has exploded over the years</b>.
            </p>
            <p style="color:{COLORS['text']}">
                The share of indie games is noticeably higher when unreliable votes are included. 
                This makes sense, as professional reviewers are often less likely to rate indie titles, 
                which means the “unverified” category tends to include a much larger number of indie releases.
            </p>
            <p style="color:{COLORS['text']}">
                Interestingly, this growth suggests that <b>indie games could soon dominate the market</b> 
                in terms of sheer volume. However, when considering only titles with reliable votes, 
                journalists still appear to favor non-indie games, indicating a bias toward 
                larger productions or more mainstream titles.
            </p>
            <p style="color:{COLORS['text']}">
                Overall, the data clearly illustrates how the indie scene has evolved 
                from a niche segment to a <b>major driving force in the gaming industry</b>.
            </p>
            <p style="font-style: italic; color: {COLORS['subtext']}; margin-top: 10px;">
                Note: You can hover over the graphs to see the exact values, 
                as these are interactive plots with hover functionality.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    
    st.markdown("---")


    col_cam_1,col_cam_2 = st.columns([1,1])

    genre_color_dict = {
        "Shooter": "#636EFA",
        "Indie": "#EF553B",
        "Arcade": "#00CC96",
        "Racing": "#AB63FA",
        "Simulator": "#FFA15A",
        "Sport": "#19D3F3",
        "Platform": "#FF6692",
        "Adventure": "#B6E880",
        "Role-playing (RPG)": "#FF97FF",
        "Strategy": "#FECB52",
        "Point-and-click": "#636EFA",
        "Visual Novel": "#EF553B",
        "Fighting": "#00CC96",
        "Puzzle": "#AB63FA",
        "Real Time Strategy (RTS)": "#FFA15A",
        "Turn-based strategy (TBS)": "#19D3F3",
        "Card & Board Game": "#FF6692",
        "Tactical": "#B6E880",
        "Music": "#FF97FF",
        "Hack and slash/Beat 'em up": "#FECB52",
        "Quiz/Trivia": "#636EFA",
        "Pinball": "#EF553B",
        "MOBA": "#00CC96"
    }

    with col_cam_1:
        df["genres"] = df["genres"].apply(lambda x: ast.literal_eval(x))
        df_novote = df[df["has_reliable_votes"] == True]
        df_genres = df_novote.explode("genres")
        genre_counts = df_genres["genres"].value_counts().reset_index()
        genre_counts.columns = ["genre", "count"]
        fig = camemberg_genres(genre_counts,"Distribution of game Genres (with reliable vote)", genre_color_dict)
        st.plotly_chart(fig)

    with col_cam_2:
        df_genres = df.explode("genres")
        genre_counts = df_genres["genres"].value_counts().reset_index()
        genre_counts.columns = ["genre", "count"]
        fig = camemberg_genres(genre_counts,"Distribution of game Genres (with rating, reliable or not)", genre_color_dict)
        st.plotly_chart(fig)

    st.markdown(
        f"""
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: {COLORS['highlight']}; margin-bottom: 15px;">
                Analysis of Game Genres Distribution
            </p>
            <p style="color:{COLORS['text']}"> 
                Here, we compare the <b>distribution of genres</b> across all released games. 
                A noticeable difference emerges between titles with reliable votes and those without, 
                echoing our previous analysis on indie games: the share of indie titles is particularly 
                high when considering all games, regardless of whether they have been rated by professional reviewers.
            </p>
            <p style="color:{COLORS['text']}">
                Furthermore, we observe a clear dominance of <b>adventure games</b>, 
                highlighting certain prevailing trends in player preferences and game development. 
                This indicates that some genres consistently attract more releases and attention from developers.
            </p>
            <p style="color:{COLORS['text']}">
                It would be particularly interesting to explore how the distribution of these genres evolves over time, 
                to identify emerging trends or shifts in gaming preferences.
            </p>
            <p style="font-style: italic; color: {COLORS['subtext']}; margin-top: 10px;">
                Note: You can hover over the graphs to see the exact numbers, 
                as these are interactive plots with hover functionality. 
                You can also click on the legend items to hide or show specific genres dynamically, 
                and scroll through the legend if it exceeds the visible area.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    year_selected = st.slider("Select year", min_value=2000, max_value=2025, value=2012)

    col_cam_3, col_cam_4 = st.columns([1,1])

    with col_cam_3:
        df_genres_reliable = df_genres[df_genres["has_reliable_votes"] == True]
        genre_counts_year = (df_genres_reliable[df_genres_reliable["first_release_date"] == year_selected].groupby("genres").size().reset_index(name="count"))
        genre_counts_year.columns = ["genre", "count"]
        fig = camemberg_genres(genre_counts_year,f"Distribution of game Genres in {year_selected} (with reliable vote)",genre_color_dict)
        st.plotly_chart(fig)

    with col_cam_4:
        genre_counts_year_all = (df_genres[df_genres["first_release_date"] == year_selected].groupby("genres").size().reset_index(name="count"))
        genre_counts_year_all.columns = ["genre", "count"]
        fig = camemberg_genres(genre_counts_year_all,f"Distribution of game Genres in {year_selected} (with rating, reliable or not)",genre_color_dict)
        st.plotly_chart(fig)


    st.markdown("---")

    st.markdown(
        f"""
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: {COLORS['highlight']}; margin-bottom: 15px;">
                Summary of Game Quantity Analysis
            </p>
            <p style="color:{COLORS['text']}">
                In this section, we can conclude the <b>Game Quantity</b> part by combining it with <b>Game Quality</b>. 
                This graph provides a wealth of information, and we strongly encourage you to explore it in detail. 
            </p>
            <p style="color:{COLORS['text']}">
                For example, we notice that the majority of <b>reliable votes</b> are connected with <b>collections</b>, 
                which shows that journalists follow licensed titles much more closely than independent games.
                We also observe that most games rated <b>90+</b> are linked to licensed titles, 
                whereas the majority of games rated below <b>60</b> tend to have <b>no reliable votes</b>. 
                This highlights a certain marginality in the video game ecosystem. 
                <b>Early Access</b> titles are also overwhelmingly represented among games without reliable votes, 
                which is understandable as they have not been officially released yet.
                Additionally, most <b>remakes</b> receive ratings above 75, often reaching 90, 
                and the majority come from collections. 
                Games with <b>2–5 DLCs</b> are usually rated above 75, 
                and <b>remasters</b> with more than 20 DLCs are mainly highly rated normal games, 
                although some remasters are present (but no remakes in this category).
            </p>
            <p style="font-style: italic; color: {COLORS['subtext']}; margin-top: 10px;">
                Note for reading the graph:<br>
                - You can reorder the columns in any way you want.<br>
                - You can rearrange the zones within a column from top to bottom as you prefer.<br>
                - Hovering over a line shows the entire path of that game.<br>
                - Hovering over a part of column shows the paths of all lines connected to that category.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    df_compar = df[["has_collections","has_reliable_votes","total_rating","dlcs"]]

    conditions = [df["remake"] == True,df["remaster"] == True,df["early_access"] == True]
    choices = ["has_remake", "has_remaster", "has_early_access"]
    df_compar["special"] = np.select(conditions, choices, default="none")

    bins = [0, 60, 75, 90, 100]
    labels = ["<60", "60–74", "75–89", "90+"]
    df_compar["total_rating"] = pd.cut(df["total_rating"], bins=bins, labels=labels)

    bins_dlcs = [-1, 0, 1, 5, 10, 20, float("inf")] 
    labels_dlcs = ["0", "1", "2–5", "6–10", "11–20", "20+"]
    df_compar["dlcs"] = pd.cut(df_compar["dlcs"], bins=bins_dlcs, labels=labels_dlcs)

    fig = parallele_comp(df_compar)
    st.plotly_chart(fig)
