# Import the required libraries
import streamlit as st
import ast

def show_home(df):
    # Introduction
    with st.container(key="intro"):
        st.title("The Evolution of Video Games in the 21st Century")
        st.subheader("Gaming Habits in Transformation")

        st.markdown(
            """
            Using the open-source **IGDB** database, we collected more than **29,000 video games** released between **January 1, 2000** and **October 1, 2025**.  
            Only games containing all the key features we needed were kept, particularly those with player ratings and/or Metacritic scores.

            In this Streamlit app, we explore and analyze how video games have evolved throughout the 21st century,  to better understand the new face of an industry constantly reinventing itself.

            **In this first section, feel free to explore the dataset.**
                                        
            <p style="font-style: italic; color: gray; margin-top: 10px;">
            Note: in our database, we have main games, remakes, remasters, and standalones, but not ports. Therefore, all definitive editions or simple PC ports are not included.
            </p>
            """,
            unsafe_allow_html=True
        )

        def safe_eval(val):
            if isinstance(val, str):
                try:
                    return ast.literal_eval(val)
                except Exception:
                    return []  
            elif isinstance(val, list):
                return val
            else:
                return []  


    with st.container(key="zone-jeu"):
        # he search bar
        col1, col2 = st.columns([0.8, 0.2])  

        with col1:
            game_name = st.text_input("Find a game:", key="search")
        
        if st.button("Explore random game", key="random"):
            game_name = df.sample(n=1)["name"].iloc[0]

        with col2:
            if game_name:
                results = df[df['name'].str.contains(game_name, case=False)]
                if results.empty:
                    st.markdown('<div class="no-results">No games</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="results-count">{len(results)} games found</div>', unsafe_allow_html=True)

    # If the game is found
    if game_name and not results.empty:
        with st.container(key="game"):
            selected_game = st.selectbox("Select a game:", results["name"])
            # Get data for the selected game
            game_data = results[results["name"] == selected_game].iloc[0]

            # Display game name
            if(game_data["early_access"]):
                st.subheader(f"{game_data["name"]} (early access)")
            else:
                st.subheader(game_data["name"])

            image_width = 250
            
            # Display cover image
            cover_url = game_data.get("cover")
            cover_url = "https:" + cover_url # Because it's start with //
            if cover_url != "https:https://i.imgur.com/VsWBrKg.jpeg":
                st.image(cover_url, caption="Official cover", width=image_width)
            else:
                st.image("https://i.imgur.com/VsWBrKg.jpeg", caption="No official cover", width=image_width)

            # Display game type 
            game_type = game_data.get("game_type")
            color_map = {
                "Remake": "#ae43a3",    
                "Remaster": "#57a4c0",   
                "Main Game": "#6a43ae",   
                "Standalone Expansion": "#ae4351"   
            }
            bg_color = color_map.get(game_type)  
            st.markdown(
                f"""
                <div style="
                    display: inline-block;
                    background-color: {bg_color};
                    color: white;
                    padding: 5px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 14px;
                    margin-top: 0px;
                ">
                    {game_type}
                </div>
                """,
                unsafe_allow_html=True
            )

            col_left, col_right = st.columns(2)

            with col_left:
                #Display release data
                st.write("First release data:", game_data.get("first_release_date"))
            
                # Display collection / remake / remaster
                collection = game_data.get("has_collections")
                collection_color = "#a0e7a0" if collection else "#f5a0a0"
                collection_text = "Y" if collection else "N"
                badges_html = f'<div style="margin-top:5px; display:flex; align-items:center; gap:10px; justify-content:center;">'
                badges_html += f'<span>Part of a collection?</span>'
                badges_html += f'<span style="background-color:{collection_color}; border-radius:10px; padding:5px 10px; font-weight:bold; color:black;">{collection_text}</span>'
                badges_html += '</div>'

                # Only for Main Game
                if game_data.get("game_type") == "Main Game":
                    # Remake
                    has_remake = game_data.get("remake", False)
                    remake_color = "#a0e7a0" if has_remake else "#f5a0a0"
                    remake_text = "Y" if has_remake else "N"
                    badges_html += f'<div style="margin-top:5px; display:flex; align-items:center; gap:10px; justify-content:center;">'
                    badges_html += f'<span>Has a remake?</span>'
                    badges_html += f'<span style="background-color:{remake_color}; border-radius:10px; padding:5px 10px; font-weight:bold; color:black;">{remake_text}</span>'
                    badges_html += '</div>'

                    # Remaster
                    has_remaster = game_data.get("remaster", False)
                    remaster_color = "#a0e7a0" if has_remaster else "#f5a0a0"
                    remaster_text = "Y" if has_remaster else "N"
                    badges_html += f'<div style="margin-top:5px; display:flex; align-items:center; gap:10px; justify-content:center;">'
                    badges_html += f'<span>Has a remaster?</span>'
                    badges_html += f'<span style="background-color:{remaster_color}; border-radius:10px; padding:5px 10px; font-weight:bold; color:black;">{remaster_text}</span>'
                    badges_html += '</div>'
                st.markdown(badges_html, unsafe_allow_html=True)

                # Display developers
                developers = safe_eval(game_data.get("developer_company"))
                developers_country = safe_eval(game_data.get("developer_country"))
                html_developers = '<div style="margin-top: 15px;"><strong>Developers:</strong><br>'
                for i, dev in enumerate(developers):
                    country = developers_country[i] if i < len(developers_country) else "N/A"
                    html_developers += f"- {dev} ({country})<br>"
                html_developers += "</div>"
                st.markdown(html_developers, unsafe_allow_html=True)

                # Display publishers
                publishers = safe_eval(game_data.get("publisher_company"))
                publishers_country = safe_eval(game_data.get("publisher_country"))
                html_publishers = '<div style="margin-top: 5px;"><strong>Publishers:</strong><br>'
                for i, pub in enumerate(publishers):
                    country = publishers_country[i] if i < len(publishers_country) else "N/A"
                    html_publishers += f"- {pub} ({country})<br>"
                html_publishers += "</div>"
                st.markdown(html_publishers, unsafe_allow_html=True)

                # Display game mod
                game_mod = safe_eval(game_data.get("game_modes"))
                html_game_mod = '<div style="margin-top: 15px;"><strong>Game mod:</strong><br>'
                for i in game_mod:
                    html_game_mod += f"- {i}<br>"
                html_game_mod += "</div>"
                st.markdown(html_game_mod, unsafe_allow_html=True)

                # Display perspectives
                player_perspectives = safe_eval(game_data.get("player_perspectives"))
                html_player_perspectives = '<div style="margin-top: 5px;"><strong>Player perspectives:</strong><br>'
                for i in player_perspectives:
                    html_player_perspectives += f"- {i}<br>"
                html_player_perspectives += "</div>"
                st.markdown(html_player_perspectives, unsafe_allow_html=True)

            with col_right:
                # Display total rating
                total_rating = round(game_data.get("total_rating", 0))
                if total_rating >= 90:
                    bg_color = "#21A671"  
                elif total_rating >= 75:
                    bg_color = "#a0e7a0"  
                elif total_rating >= 60:
                    bg_color = "#fff5a0"  
                else:
                    bg_color = "#f5a0a0" 
                st.markdown(
                    f"""
                    <span style="display: inline-flex; align-items: center; gap: 10px;">
                        <span>Rating:</span>
                        <span style="
                            background-color: {bg_color};
                            border-radius: 10px;
                            padding: 5px 10px;
                            font-weight: bold;
                            color: black;
                        ">
                            {total_rating} / 100
                        </span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                # Display age ranking
                age_rating = game_data.get("age_rattings")
                if age_rating.lower() in ["everyone"]:
                    badge_color = "#a0e7a0" 
                elif age_rating.lower() in ["child"]:
                    badge_color = "#add8e6" 
                elif age_rating.lower() in ["teen"]:
                    badge_color = "#fff5a0" 
                elif age_rating.lower() in ["young"]:
                    badge_color = "#ffa500"  
                elif age_rating.lower() in ["18+"]:
                    badge_color = "#f5a0a0"  
                st.markdown(
                    f"""
                    <span style="display: inline-flex; align-items: center; gap: 10px; margin-top: 10px">
                        <span>Age rating:</span>
                        <span style="
                            background-color: {badge_color};
                            border-radius: 10px;
                            padding: 5px 10px;
                            font-weight: bold;
                            color: black;
                        ">
                            {age_rating}
                        </span>
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                # Display platform 
                platforms = safe_eval(game_data.get("platforms"))
                platform_family = safe_eval(game_data.get("platform_family"))
                html_platforms = '<div style="margin-top: 15px;"><strong>Platforms:</strong><br>'
                for i, plat in enumerate(platforms):
                    family = platform_family[i] if i < len(platform_family) else "N/A"
                    html_platforms += f"- {plat} ({family})<br>"
                html_platforms += "</div>"
                st.markdown(html_platforms, unsafe_allow_html=True)

                # Display type platform
                platform_type = safe_eval(game_data.get("platform_type"))
                html_platforms_type = '<div style="margin-top: 5px; margin-bottom: 5px"><strong>Platform type:</strong><br>'
                for i in platform_type:
                    html_platforms_type += f"- {i}<br>"
                html_platforms_type += "</div>"
                st.markdown(html_platforms_type, unsafe_allow_html=True)

                # Display generation platform
                generation = game_data.get("generation_platform")
                if generation != 0:
                    st.write(f"Generation: {generation}")

                # Display type genre
                genre = safe_eval(game_data.get("genres"))
                html_genre = '<div style="margin-bottom: 15px"><strong>Genres:</strong><br>'
                for i in genre:
                    html_genre += f"- {i}<br>"
                html_genre += "</div>"
                st.markdown(html_genre, unsafe_allow_html=True)

                # Display dlcs
                st.write(f"Number dlcs: {game_data.get("dlcs")}")

    st.markdown("---")

    st.markdown(
        """
        <div style="text-align: center; margin-top: 10px; margin-bottom: 3vh; font-style: italic;">
        Data preprocessing and feature extraction were carried out in a separate Jupyter Notebook to ensure data quality and reproducibility.  
        The Streamlit app focuses on storytelling and interactivity, using the cleaned dataset for smooth exploration and visualization.
        </div>
        """,unsafe_allow_html=True
    )

    # Initialize session state
    if "show_df" not in st.session_state:
        st.session_state.show_df = False

    with st.container(key="btn"):
        # Button to show dataset
        if st.button("Explore all dataset", key="explore_btn"):
            st.session_state.show_df = True

        # Download button (toujours visible)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download dataset",
            data=csv,
            file_name="games.csv",
            mime='text/csv',
            key="download_btn"
        )

    # Display dataset if flag is True
    if st.session_state.show_df:
        st.dataframe(df)