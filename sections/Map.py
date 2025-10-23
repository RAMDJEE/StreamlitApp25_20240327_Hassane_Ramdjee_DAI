# Import the required libraries
import streamlit as st
import pandas as pd
import ast
import pycountry

# Import the various functions
from utils.visualisation_map import map_general
from utils.visualisation_map import map_general_year
from utils.visualisation_map import camemberg


def show_map(df):
    st.title("The world of video games: Developer and Publisher")

    st.markdown(
        """
        On this page, we will take a closer look at the distribution of video games across different domains. Understanding **who makes and who publishes games** is crucial, as it reveals patterns of creativity, market dynamics, and the global influence of the video game industry.  

        This page is divided into two main parts:

        1. **World maps** - These maps will highlight the **geographical evolution of developers and publishers**, showing where games are being created and which regions dominate the industry over time. 

        2. **Tables by platform and company** - Here, we will focus on the **distribution by console and by company**, providing a more detailed view of industry specialization. 

        By combining these two perspectives, we gain a broader understanding of the video game ecosystem. Video games are not only a source of entertainment; they are also the **largest entertainment industry in terms of revenue**, and this is clearly reflected in the influence of certain companies and countries.  
        """,
        unsafe_allow_html=True
    )

    map1, gen = st.columns([0.75,0.25])

    # explode list of country (developer and publisher)
    def explode_country(df_proc, country, type, by_year=False):
        df_proc[country] = df_proc[country].replace("Unknown", "[]")
        df_proc[country] = df_proc[country].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else []))

        if by_year:
            return df_proc.explode(country)[[country, "year"]].rename(columns={country: "country"}).assign(type=type)
        else:
            return df_proc.explode(country)[country].rename("country").to_frame().assign(type=type)

    with gen:
        no_reliable = st.checkbox("Disable reliable votes (Warning: by disabling this, many small indie companies haven't specified their country, which can skew the results)")
        by_year = st.checkbox("If you prefer to see the number of releases per year (by default, uncheck to show all releases from 2000 to 2025)")
        df["first_release_date"] = pd.to_datetime(df["first_release_date"])
        df["year"] = df["first_release_date"].dt.year

    with map1:
        def process_countries(df, no_reliable=False, by_year=False):
            df_proc = df.copy()    

            # reliable or not
            if not no_reliable:
                df_proc = df_proc[df_proc["has_reliable_votes"] == True]
            
            # by year or global
            if by_year:
                df_proc["first_release_date"] = pd.to_datetime(df_proc["first_release_date"], errors="coerce")
                df_proc["year"] = df_proc["first_release_date"].dt.year
            
            df_devs = explode_country(df_proc, "developer_country", "developer", by_year)
            df_pubs = explode_country(df_proc, "publisher_country", "publisher", by_year)

            # iso code for the map
            def get_iso_alpha(country_name):
                try:
                    return pycountry.countries.lookup(country_name).alpha_3
                except:
                    return None
            
            df_countries = pd.concat([df_devs, df_pubs], ignore_index=True)
            df_countries["iso_alpha"] = df_countries["country"].apply(get_iso_alpha)
            
            # group of columns 
            group = ["country", "iso_alpha", "type"]
            if by_year:
                group.append("year")
            
            df_countries = df_countries.groupby(group).size().reset_index(name="count")
            
            # We need total sum of developer + publisher
            pivot_index = ["country", "iso_alpha"]
            if by_year:
                pivot_index.append("year")
            
            df_countries_map = df_countries.pivot_table(index=pivot_index,columns="type",values="count",fill_value=0).reset_index()
            df_countries_map["total"] = df_countries_map["developer"] + df_countries_map["publisher"]
            
            # Sort year 
            if by_year:
                df_countries_map = df_countries_map.sort_values("year").reset_index(drop=True)
            
            return df_countries_map

        if by_year:
            df_map = process_countries(df, no_reliable, True)
            if no_reliable:
                title = "Distribution of developer / publisher by country and year (with rating, reliable or not)"
            else:
                title = "Distribution of developer / publisher by country and year (only reliable votes)"
            fig = map_general_year(df_map, title)
        else:
            df_map = process_countries(df, no_reliable, False)
            if no_reliable:
                title = "Distribution of developer / publisher by country (with rating, reliable or not)"
            else:
                title = "Distribution of developer / publisher by country (only reliable votes)"
            fig = map_general(df_map, title)

        st.plotly_chart(fig)
    
    st.markdown(
        """
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: #553cc4; margin-bottom: 15px;">
                Global Video Game Market Dominance
            </p>
            <p>
                The dominance of the United States and Japan in the video game sector is undeniable, 
                whether we look at the overall statistics or the year-by-year breakdown. 
                However, it is worth noting that three other countries also have a significant market presence, 
                even if smaller: Canada, France, and the United Kingdom. 
                Overall, this concentration remains largely within Western countries, 
                which aligns with the notion of "gaming for the wealthy".
            </p>
            <p>
                When journalist scores are disregarded, we observe a substantial rise in Eastern Europe, 
                particularly Russia, as well as Australia, highlighting a notable share of indie games 
                emerging from these regions. Nevertheless, the United States also sees a strong increase, 
                further confirming its role in market dominance.
            </p>
            <p style="font-style: italic; color: gray; margin-top: 10px;">
                Notes:<br>
                - For reliable votes only, no country data is missing.<br>
                - When combining reliable and non-reliable votes, about a quarter of the database is missing, 
                making it difficult to analyze indie games accurately. 
                As a result, indie games are not specifically highlighted here to avoid misleading conclusions.<br>           
                - You can hover over the map to see exact values.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    st.markdown(
        """
        <div style="padding: 25px 35px; text-align: justify; font-size: 16px; line-height: 1.6;">
            <p style="font-weight: bold; font-size: 18px; color: #d43838; margin-bottom: 15px;">
                Detailed Exploration of Developer and Platform Releases
            </p>
            <p>
                We can now take a closer look at the releases from each developer across 
                different platforms. This section allows for an in-depth exploration of 
                the market, giving you the flexibility to analyze trends according to your own criteria.
                You can:
                <ul style="margin-top: 10px; margin-bottom: 10px;">
                    <li><strong>Include only reliable votes</strong>: limit results to games with verified critic scores.</li>
                    <li><strong>Select a specific developer</strong>: focus on releases from one studio only.</li>
                    <li><strong>Filter by publisher</strong>: examine the output of a single publishing company.</li>
                    <li><strong>Choose a console family</strong>: restrict the dataset to Nintendo, PlayStation, or Xbox platforms.</li>
                    <li><strong>Enable “Only exclusives”</strong>: display games released solely on the selected console family.</li>
                    <li><strong>Include PC releases</strong>: when enabled, games released both on PC and a single console are still considered as “exclusives”.</li>
                    <li><strong>Activate backward compatibility</strong>: include titles that were released on previous generations of the selected platform family.</li>
                    <li><strong>Pick a specific platform</strong>: narrow down results to one console (e.g., PS4, Switch, Xbox 360, etc.).</li>
                    <li><strong>Explore a category</strong>: analyze by genres, age ratings, or game type.</li>
                    <li><strong>Activate all options</strong>: get a complete overview without any filter.</li>
                </ul>
            </p>
            <p>
                This gives you <strong>extensive control</strong> over the filters and the type of analysis 
                you wish to conduct. Feel free to experiment with different combinations to uncover 
                interesting relationships between studios, platforms, and genres.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([0.7,0.3])

    with col2:
        # choice : categories
        liste = ["game_type", "age_rattings", "genres"]
        categories = st.selectbox("Select a category:",liste)

        # Choice: only reliable
        reliable_only = st.checkbox("Include only reliable votes")

        # Choice: developers
        developer_all = st.checkbox("All developers", value=True)
        developer = st.text_input("Find a developer:", disabled=developer_all)
        if developer.strip():
            results_df_dev = explode_country(df, "developer_company", "developer")
            stock_dev = results_df_dev[results_df_dev["country"].str.contains(developer, case=False, na=False)]
            results_dev = stock_dev["country"].unique().tolist()
        else:
            results_dev = []
        selected_game_dev = st.selectbox("Select a developer:", results_dev, disabled=developer_all or not developer.strip())

        # Choice: publishers
        publisher_all = st.checkbox("All publishers", value=True)
        publisher = st.text_input("Find a publisher:", disabled=publisher_all)
        if publisher.strip():
            results_df_pub = explode_country(df, "publisher_company", "publisher")
            stock_pub = results_df_pub[results_df_pub["country"].str.contains(publisher, case=False, na=False)]
            results_pub = stock_pub["country"].unique().tolist()
        else:
            results_pub = []
        selected_game_pub = st.selectbox("Select a publisher:", results_pub, disabled=publisher_all or not publisher.strip())

        # Choice: platform family (the 3 big)
        platform_fam = ["Nintendo","PlayStation","Xbox"]
        platform_fam_all = st.checkbox("All platforms families", value=True)
        selected_platform_fam = st.selectbox("Select a platform family:", platform_fam, disabled=platform_fam_all)

        # Choice: pc and exclu? 
        is_exclu = st.checkbox("Only exclu?", disabled=platform_fam_all)
        pc = st.checkbox("PC releases?", disabled=not is_exclu)

        # Choice: precise platform
        df["platform_family"] = df["platform_family"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else []))
        df["platforms"] = df["platforms"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else []))
        df_filtered = df[df["platform_family"].apply(lambda lst: set(lst) == {selected_platform_fam})]
        excluded_platforms = {
            "Windows Phone", "Legacy Mobile Device", "Web browser", "BlackBerry OS",
            "WonderSwan Color", "Neo Geo Pocket Color", "MSX", "Gizmondo", "Digiblast",
            "Arcade", "64DD", "Family Computer", "Oculus Quest", "visionOS", "Zeebo",
            "SteamVR", "Gear VR", "Meta Quest 3", "Oculus Go", "Windows Mixed Reality",
            "Oculus VR", "Daydream", "Meta Quest 2", "Oculus Rift"
        }
        all_platforms = set(p for sublist in df_filtered["platforms"] for p in sublist if p not in excluded_platforms)
        
        is_platform = st.checkbox("All platform of this family?", disabled=platform_fam_all, value=True)
        selected_platform = st.selectbox("Select a platform:", all_platforms, disabled=is_platform)
        full_exclu = st.checkbox("Backward compatibility?", disabled=is_platform)

    with col1:
        df_final = df.copy()  

        # df with reliable
        if(reliable_only):
            df_final = df_final[df_final["has_reliable_votes"] == True]
        
        # df with developers
        if(not developer_all):
            df_final = df_final[df_final["developer_company"].apply(lambda lst: selected_game_dev in (lst if isinstance(lst, list) else []))]
        
        # df with publishers
        if(not publisher_all):
            df_final = df_final[df_final["publisher_company"].apply(lambda lst: selected_game_pub in (lst if isinstance(lst, list) else []))]
        
        if df_final.empty:
            df_final = pd.DataFrame(columns=df.columns)

        # df with platform family
        if not platform_fam_all:
            df_final["platform_family"] = df_final["platform_family"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else []))

            if is_exclu:
                if not pc:
                    df_final = df_final[df_final["platform_family"].apply(lambda lst: set(lst) == {selected_platform_fam})]
                else:
                    df_final = df_final[df_final["platform_family"].apply(lambda lst: set(lst) == {selected_platform_fam} or set(lst) == {selected_platform_fam, "Windows"})]
            else:
                df_final = df_final[df_final["platform_family"].apply(lambda lst: selected_platform_fam in lst)]
        
        if df_final.empty:
            df_final = pd.DataFrame(columns=df.columns)
        
        # df with platform
        if not is_platform:
            df_final["platforms"] = df_final["platforms"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else (x if isinstance(x, list) else []))
            
            if not full_exclu:
                if not pc:
                    df_final = df_final[df_final["platforms"].apply(lambda lst: set(lst) == {selected_platform})]
                else:
                    df_final = df_final[df_final["platforms"].apply(lambda lst: set(lst) == {selected_platform} or set(lst) == {selected_platform, "PC"})]
            else:
                if not pc:
                    df_final = df_final[df_final["platforms"].apply(lambda lst: selected_platform in lst)]
                else:
                    df_final = df_final[df_final["platforms"].apply(lambda lst: selected_platform in lst or "PC" in lst)]
        
        if df_final.empty:
            df_final = pd.DataFrame(columns=df.columns)

        # pie 
        df_final["genres"] = df_final["genres"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        if categories == "genres":
            df_genres = df_final.explode("genres")
            df_pie = df_genres.groupby("genres").size().reset_index(name="count")
        else:
            df_pie = df_final.groupby(categories).size().reset_index(name="count")

        fig = camemberg(df_pie, categories)
        st.plotly_chart(fig)
    
        df_final = df_final.sort_values("first_release_date")
        st.write(f"Number of filtered games: {len(df_final)}")
        st.dataframe(df_final)
