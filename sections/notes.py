# Import the required libraries
import streamlit as st
import ast

# Import the various functions
from utils.visualisation_quality import plot_average_rating
from utils.visualisation_quality import plot_average_rating_collection
from utils.visualisation_quality import plot_average_rating_genre
from utils.visualisation_quality import plot_average_rating_companies_exclu
from utils.visualisation_quality import plot_top10
from utils.visualisation_quality import camembert_grouped

def show_notes(df):
    # Title and introduction 
    st.title("Distribution of Ratings")

    # Introduction
    st.markdown(
        """
        One of the central aspects of video games lies in the ratings they receive. 
        These ratings give us a first idea of a game's quality. 
        But a legitimate question to ask is: *"How can game criteria influence ratings?"* 
        From this, we can observe trends throughout the 21st century that may emerge.
        
        **Note:** 
        - Ratings in our database are divided by reliability. A rating that averages professional and player scores is considered reliable.
        - Some ratings come from IGDB (which manages this database) due to a lack of professional reviews and are therefore less reliable. 
        Ratings based solely on player scores are considered unreliable. 
        By checking the box below, you will only use the most reliable ratings, but be aware that they cover only about a quarter of the database.
        """
    )

    # Interactive filter
    only_reliable = st.checkbox("Show only reliable votes")

    # First graph
    st.markdown(
        """
        Our working dataset in this study will be the average game ratings per year. 
        This will allow us to observe the evolution over time, as well as the distribution across genres, developers, etc.

        But let's start with the basics and look at the yearly averages first!
        """
    )

    # We calculate the average and store it
    df_rating = df[["first_release_date", "total_rating", "has_reliable_votes"]]
    df_rating["first_release_date"] = df["first_release_date"].dt.year
    mean_by_year = df_rating.groupby(["first_release_date","has_reliable_votes"])["total_rating"].mean().reset_index()
    mean_by_year.columns = ["year", "has_reliable_votes", "average_rating"]

    # Analyse 
    st.markdown(
        """
        <div style="margin-bottom: 3vh;">
        On this graph, we see a similar trend whether or not we filter for reliable votes: in the last five years, the <strong>average video game ratings</strong> have been higher than the <strong>global average</strong> (dashed line) over the past 25 years.  
        This is interesting because, in popular opinion, it is often said that the quality of games has declined in recent years.  
        Do these ratings truly reflect game quality? At this stage, we cannot say for sure, and further analysis will be needed.  

        It is now relevant to look at the distribution of ratings according to various criteria.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display : Average Game Rating by Release Year
    fig = plot_average_rating(mean_by_year, only_reliable)
    st.pyplot(fig)

    st.markdown("---")

    col_left_collect, col_right_collect = st.columns([3,1])

    with col_left_collect:
        # We calculate the average and store it (with collections)
        df_rating_collect = df[["first_release_date", "total_rating", "has_reliable_votes", "has_collections"]]
        df_rating_collect["first_release_date"] = df["first_release_date"].dt.year
        mean_by_year_collect = df_rating_collect.groupby(["first_release_date","has_reliable_votes", "has_collections"])["total_rating"].mean().reset_index()
        mean_by_year_collect.columns = ["year", "has_reliable_votes", "has_collections","average_rating"]

        # Display : Average Game Rating by Release Year (by Collection)
        fig = plot_average_rating_collection(mean_by_year_collect, only_reliable)
        st.pyplot(fig)

    with col_right_collect:
        # Create a summary table of counts
        if(only_reliable):
            filtered_df_collections = df_rating_collect[df_rating_collect["has_reliable_votes"] == True]
            collection_count = (filtered_df_collections.groupby(["first_release_date", "has_collections"]).size().reset_index(name="count").pivot(index="first_release_date", columns="has_collections", values="count").astype(int).rename(columns={True: "Collections", False: "Non-Collections"}))
        else:
            collection_count = (df_rating_collect.groupby(["first_release_date", "has_collections"]).size().reset_index(name="count").pivot(index="first_release_date", columns="has_collections", values="count").astype(int).rename(columns={True: "Collections", False: "Non-Collections"}))
        st.markdown("### Number of Games per Year (Collections)")
        st.dataframe(collection_count, use_container_width=True)
    
    # Analyse
    st.markdown(
        """
        <div style=" padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: #553cc4; margin-bottom: 15px;">
                Games in a Collection vs Standalone Titles
            </p>
            <p>
                On this graph, we can observe the ratings depending on whether a game is part of a collection,
                meaning whether other games exist within the same universe. 
                The interesting point in this study is to see whether being part of a collection actually influences ratings, 
                and indeed it does: across all years, games that belong to a collection consistently have 
                higher average ratings than standalone titles. 
            </p>
            <p>
                This can be explained by several factors such as brand popularity, 
                an already well-established gameplay formula, or player familiarity with the universe.
            </p>
            <p>
                Nevertheless, whether a game is part of a collection or not, 
                the general trend over time remains the same: a steady increase in average ratings.
            </p>
            <p>
                We have also added a small section on the <b>number of games released per year</b> on the side, 
                to highlight a potential bias in interpretation. 
                We will explore this aspect in more detail in a later section, 
                but it’s important to keep this factor in mind when analyzing the trends.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col_left_genre, col_right_genre = st.columns([3,1])

    with col_left_genre:
        # We calculate the average and store it (with indie)
        df_rating_genres = df[["first_release_date", "total_rating", "has_reliable_votes", "genres", "name"]]
        df_rating_genres["first_release_date"] = df["first_release_date"].dt.year
        df_rating_genres["genres"] = df_rating_genres["genres"].apply(lambda x: ast.literal_eval(x))
        df_rating_genres["is_indie"] = df_rating_genres["genres"].apply(lambda x: "Indie" in x if isinstance(x, list) else False)
        mean_by_year_indie = (df_rating_genres.groupby(["first_release_date", "has_reliable_votes", "is_indie"])["total_rating"].mean().reset_index())
        mean_by_year_indie.columns = ["year", "has_reliable_votes", "is_indie","average_rating"]

        # Display : Average Game Rating by Release Year (by indie)
        fig = plot_average_rating_genre(mean_by_year_indie, only_reliable)
        st.pyplot(fig)

    with col_right_genre:
        # Create a summary table of counts
        if(only_reliable):
            filtered_df_genres = df_rating_genres[df_rating_genres["has_reliable_votes"] == True]
            indie_counts = (filtered_df_genres.groupby(["first_release_date", "is_indie"]).size().reset_index(name="count").pivot(index="first_release_date", columns="is_indie", values="count").fillna(0).astype(int).rename(columns={True: "Indie", False: "Non-Indie"}))
        else:
            indie_counts = (df_rating_genres.groupby(["first_release_date", "is_indie"]).size().reset_index(name="count").pivot(index="first_release_date", columns="is_indie", values="count").astype(int).rename(columns={True: "Indie", False: "Non-Indie"}))
        st.markdown("### Number of Games per Year (Indie)")
        st.dataframe(indie_counts, use_container_width=True) 

    # Analyse
    st.markdown(
        """
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: #924ea7; margin-bottom: 15px;">
                Indie Games vs Non-Indie Titles
            </p>
            <p>
                In this graph, we focus on <b>Indie games</b> and how their ratings compare to non-indie titles over time. 
                It’s particularly interesting to look at both the filtered and unfiltered views regarding reliable votes, 
                since most titles affected by this filter belong to the indie category. 
                We can also note that the number of games marked as reliable is significantly low (see the table on the right). 
                This highlights that indie games in the early 2000s were not popular at all, resulting in a complete absence of professional ratings (which we will revisit later).
            </p>
            <p>
                Therefore, the early 2000s must be interpreted carefully, as this biases the average rating. 
                From 2010 onward, the ratings between indie and non-indie games remain fairly close, 
                although indie games fall behind non-indie games in 2015. 
            </p>
            <p>
                This can be explained by the <b>rapid growth of the indie scene</b> in recent years: 
                a higher volume of indie releases also brings greater variability in quality, 
                as many creators attempt to develop games without extensive experience or resources. 
            </p>
            <p>
                However, the recent surge in popularity is also reflected in the ratings of recent years, 
                where indie games manage to match or even surpass non-indie titles.
            </p>
            <p>
                Despite these differences, the overall trend remains consistent: 
                average ratings have been <b>steadily increasing over the years</b>, 
                regardless of whether a game is indie or not.
            </p>
            <p>
                This confirms the broader observation that <b>the general upward trend in ratings</b> 
                applies to all game categories: collected or not, indie or not.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col_left_platforms, col_right_platforms = st.columns([3,1])

    with col_right_platforms:
        names_list = {name for sublist in df["platform_family"].apply(ast.literal_eval) for name in sublist}
        name = st.selectbox(
            "Choose a platform",
            options=names_list,
            index=0,  
            help="Select only one platform"
        )

    with col_left_platforms:
        # We calculate the average and store it (with platforms)
        df_rating_platforms = df[["first_release_date", "total_rating", "has_reliable_votes", "platform_family"]]
        df_rating_platforms["first_release_date"] = df["first_release_date"].dt.year
        df_rating_platforms["platform_family"] = df_rating_platforms["platform_family"].apply(lambda x: ast.literal_eval(x))
        df_rating_platforms["platform_family"] = df_rating_platforms["platform_family"].apply(lambda x: list(set(x)))
        df_rating_platforms = df_rating_platforms[df_rating_platforms["platform_family"].apply(lambda x: name in x)]
        df_rating_platforms["is_exclu"] = df_rating_platforms["platform_family"].apply(lambda x: True if x == [name] else False)
        mean_by_year_platforms = (df_rating_platforms.groupby(["first_release_date", "has_reliable_votes", "is_exclu"])["total_rating"].mean().reset_index())
        mean_by_year_platforms.columns = ["year", "has_reliable_votes", "is_exclu", "average_rating"]
        
        # Display : Average Game Rating by Release Year (by name and exclu)
        fig = plot_average_rating_companies_exclu(mean_by_year_platforms, name, only_reliable)
        st.pyplot(fig)

    st.markdown(
        """
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: #4e79a7; margin-bottom: 15px;">
                Game Ratings by Platform & Exclusivity
            </p>
            <p>
                In this section, we examine the <b>average ratings per game platform</b>. 
                Naturally, quality is influenced by quantity, but we will address volume in a separate section; 
                here, we focus purely on the ratings themselves.
            </p>
            <p>
                We differentiate between <b>exclusive</b> and <b>non-exclusive</b> games, meaning whether a title is available 
                only on the platform in question and nowhere else. 
                Note that by "platform" we refer to the platform family: 
                a game released on both PS4 and PS5 is considered an exclusive for this analysis.
            </p>
            <p>
                Trends vary by company, and we encourage exploration of the dataset. 
                However, we can observe that console prestige, particularly <b>Nintendo</b> and <b>PlayStation</b>, 
                is reflected in very high ratings for exclusives. 
                Conversely, platforms considered in decline, such as <b>Sega</b> and <b>Microsoft</b>, 
                often show weak or non-existent exclusive ratings.
            </p>
            <p>
                Nevertheless, this dominance of exclusives can vary significantly depending on whether the ratings are considered reliable or not. 
                We strongly encourage examining both views during analyses. Exclusive games tend to always receive professional reviews, 
                which substantially affects average ratings and the presence of games in the dataset.
            </p>
            <p>
                For <b>Windows</b>, the parity between exclusive and non-exclusive ratings is largely due to the presence of indie games 
                (PC exclusives) and multi-platform titles. 
                Windows highlights the overall upward trend in ratings observed throughout this analysis, 
                especially when including all games, not just those with reliable votes. 
                This effect is further accentuated by Nintendo and PlayStation, which continue to drive the trend upward.
            </p>
            <p>
                Of course, Nintendo and PlayStation also achieve such high ratings because the number of exclusive games released each year is relatively low (a topic we’ll explore in the next section): fewer titles, but almost flawless quality.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: #4e79a7; margin-bottom: 15px;">
                Visualizations of Distributions
            </p>
            <p>
                Here, you can freely explore the distribution of age classes, the share of collections, and whether games are solo or multiplayer. Games are ranked according to their top ratings. 
            </p>
            <p>
                Therefore, if you set "1000" on the slider, the top 1000 will be displayed, and you can view the distribution you want to examine. 
            </p>
            <p>
                Note that, once again, <b>reliable votes</b> influence the top rankings you can view.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    colpie, colcursor = st.columns([1,1])
    with colcursor:
        if(only_reliable):
            number = st.slider("Choose a grade threshold:", min_value=100, max_value=6500, value=3300, step=100)
        else:
            number = st.slider("Choose a grade threshold:", min_value=500, max_value=28500, value=14500, step=500)
    
        category_choice = st.selectbox("Select a category group:", ["has_collections", "game_modes", "age_ratings"])
        category_map = {
            "has_collections": ["has_collections"],
            "game_modes": ["has_single_player", "has_multi", "has_both", "has_other"],
            "age_ratings": ["age_everyone", "age_child", "age_teen", "age_young", "age_18plus"]
        }
        pretty_labels = {
            "has_collections": "Collection",
            "has_single_player": "Single Player",
            "has_multi": "Multiplayer / Co-op",
            "has_both": "Both Modes",
            "has_other": "Other Modes",
            "age_everyone": "Everyone",
            "age_child": "Child",
            "age_teen": "Teen",
            "age_young": "Young",
            "age_18plus": "18+"
        }

    with colpie:
        df_pie = df[["total_rating","has_collections","has_reliable_votes"]].copy()

        df_stock = df["game_modes"].apply(lambda x: ast.literal_eval(x))
        df_pie["has_single_player"] = df_stock.apply(lambda modes: len(modes) == 1 and modes[0] == "Single player")
        df_pie["has_multi"] = df_stock.apply(lambda modes: len(modes) == 1 and modes[0] in ["Multiplayer", "Co-operative"])
        df_pie["has_both"] = df_stock.apply(lambda modes: len(modes) >= 2 and any(m in ["Single player", "Multiplayer", "Co-operative"] for m in modes))
        df_pie["has_other"] = df_stock.apply(lambda modes: not (len(modes) == 1 and modes[0] == "Single player") and not (len(modes) == 1 and modes[0] in ["Multiplayer", "Co-operative"]) and not (len(modes) >= 2 and any(m in ["Single Ppayer", "Multiplayer", "Co-operative"] for m in modes)))

        df_pie["age_everyone"] = df["age_rattings"] == "Everyone"
        df_pie["age_child"] = df["age_rattings"] == "Child"
        df_pie["age_teen"] = df["age_rattings"] == "Teen"
        df_pie["age_young"] = df["age_rattings"] == "Young"
        df_pie["age_18plus"] = df["age_rattings"] == "18+"

        df_pie = df_pie.sort_values(by="total_rating", ascending=False)

    with colpie:
        fig = camembert_grouped(df_pie,number,category_choice,category_map,pretty_labels,only_reliable)
        st.pyplot(fig)


    st.markdown("---")

    # TOP 15
    st.markdown(
        """
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: #4e79a7; margin-bottom: 15px;">
                Top 15 Games by Category
            </p>
            <p>
                To conclude this section, we present four Top 15 lists, providing statistics on which games dominate ratings within their category. 
                It is strongly recommended to enable <b>only reliable votes</b>, since games with unreliable ratings can appear artificially high due to having very few public votes. 
            </p>
            <p>
                The four Top 15 lists are as follows: games that are part of a collection, games that are not part of any collection, 
                indie games, and console exclusives. This allows for a more nuanced view of which titles consistently perform well across different segments of the gaming landscape.
            </p>
            <p style="font-style: italic; color: gray; margin-top: 10px;">
                Note: If you have trouble reading due to your screen, remember that by hovering your mouse over the graph, you can view it in fullscreen.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    
    col_top1, col_top2 = st.columns([1,1])
    
    with col_top1:
        top10_collect = df[df["has_collections"] == True][["name","total_rating", "has_reliable_votes"]].copy()
        top10_collect["total_rating"] = top10_collect["total_rating"].round(2)
        top10_collect = top10_collect.sort_values(by="total_rating", ascending=False)

        # Display : Top 10 (collection)
        fig = plot_top10(top10_collect, "flare", only_reliable)
        st.pyplot(fig)
    
    with col_top2:
        top10_no_collect = df[df["has_collections"] == False][["name","total_rating", "has_reliable_votes"]].copy()
        top10_no_collect["total_rating"] = top10_no_collect["total_rating"].round(2)
        top10_no_collect = top10_no_collect.sort_values(by="total_rating", ascending=False)

        # Display : Top 10 (no collection)
        fig = plot_top10(top10_no_collect, "crest", only_reliable)
        st.pyplot(fig)

    col_top3, col_top4 = st.columns([1, 1])

    with col_top3:
        top10_indie = df_rating_genres[df_rating_genres["is_indie"] == True][["name", "total_rating", "has_reliable_votes"]].copy()
        top10_indie["total_rating"] = top10_indie["total_rating"].round(2)
        top10_indie = top10_indie.sort_values(by="total_rating", ascending=False)

        fig = plot_top10(top10_indie, "magma", only_reliable)
        st.pyplot(fig)

    with col_top4:
        df_rating_platforms_exclu = df[["name", "first_release_date", "total_rating", "has_reliable_votes", "platform_family"]].copy()
        df_rating_platforms_exclu["first_release_date"] = df_rating_platforms_exclu["first_release_date"].dt.year
        df_rating_platforms_exclu["platform_family"] = df_rating_platforms_exclu["platform_family"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        df_rating_platforms_exclu["platform_family"] = df_rating_platforms_exclu["platform_family"].apply(lambda x: list(set(x)) if isinstance(x, list) else [])
        df_rating_platforms_exclu["is_exclu"] = df_rating_platforms_exclu["platform_family"].apply(lambda x: len(x) == 1)
        df_rating_platforms_exclu["total_rating"] = df_rating_platforms_exclu["total_rating"].round(2)
        top10_exclu = df_rating_platforms_exclu[df_rating_platforms_exclu["is_exclu"] == True][["name", "total_rating", "has_reliable_votes"]].copy()
        top10_exclu = top10_exclu.sort_values(by="total_rating", ascending=False)

        fig = plot_top10(top10_exclu, palette="viridis", excluded_categories=only_reliable)
        st.pyplot(fig)