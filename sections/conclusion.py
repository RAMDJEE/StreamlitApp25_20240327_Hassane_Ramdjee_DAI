import streamlit as st

def show_conclusion(df,COLORS):
    with st.container(key="intro"):
        st.title("Conclusion and Future Perspectives")
        st.subheader("Reflecting on the Evolution of Video Games")

        st.markdown(
            f"""
            <div style="color:{COLORS['text']}">
            Over the course of this exploration, we analyzed how video games have evolved 
            between <strong>2000 and 2025</strong>, using data from the <strong>IGDB (Internet Games Database)</strong>, 
            an open and publicly available database maintained by the gaming community and developers.  

            This dataset was used under its open data policy and for purely <strong>educational and analytical purposes</strong>.  
            All information shown here (publishers, developers, genres, platforms, etc.) comes directly from IGDB, 
            which grants access for non-commercial data visualization and research projects.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    with st.container():
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 16px; line-height: 1.6; margin-top: 20px; color:{COLORS['text']}">
                <p style="font-weight: bold; font-size: 18px; color: {COLORS['highlight']}; margin-bottom: 15px;">
                    Areas for Improvement and Future Research
                </p>
                <p>
                    While this project provides a broad overview of the modern video game landscape, 
                    several areas could be expanded with richer data sources or complementary research:
                </p>
                <p>
                    <strong>Gender representation in video games</strong>:  
                    Unfortunately, the IGDB database does not provide information on the gender of main characters.  
                    This makes it impossible to study how the share of female protagonists or diverse representation 
                    has evolved over time.  
                    Such analysis would offer valuable insight into inclusivity and cultural change in the industry.
                </p>
                <p>
                    <strong>Better coverage of indie games</strong>:  
                    IGDB contains many indie titles, but often with incomplete metadata (developer country, publisher, 
                    or ratings missing).  
                    As a result, the influence and evolution of independent development
                    remain difficult to quantify precisely.
                </p>
                <p>
                    Expanding these dimensions would help paint a fuller picture of the 
                    <strong>social, cultural, and creative evolution</strong> of the gaming world.  
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    with st.container():
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 16px; line-height: 1.6; margin-top: 20px; color:{COLORS['text']}">
                <p>
                    <strong>Thank you for exploring the world of video games!</strong>  
                    This Streamlit app was created as a data storytelling project, combining 
                    statistics, visualization, and interactivity to highlight how the video game 
                    industry has evolved over the past 25 years.
                </p>
                <p style="font-style: italic; color:{COLORS['subtext']}; margin-top: 10px;">
                    Data cleaning and preprocessing performed in Python / Jupyter Notebook.  
                    Visualization and interface developed with Streamlit, Plotly and Seaborn.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
