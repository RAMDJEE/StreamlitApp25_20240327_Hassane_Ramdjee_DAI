## The functions that will be used on the quantity.py page

# Import the required libraries
import plotly.express as px


def plot_general(df,color,title):
    fig = px.line(
        df,
        x="first_release_date",
        y="number_of_games",
        labels={"first_release_date": "Year", "number_of_games": "Number of Games"},
        title=title,
        markers=True
    )

    fig.update_layout(
        xaxis=dict(dtick=1),          
    )

    fig.update_traces(
        line=dict(color=color)
    )

    return fig


def plot_by_indie(df, title):
    fig = px.bar(
        df,
        x="first_release_date", 
        y="number_of_games_indie", 
        color="is_indie",
        color_discrete_sequence=["#553cc4", "#924ea7"],
        pattern_shape="is_indie", 
        pattern_shape_sequence=["x", "+"],
        title=title,
        labels={"first_release_date": "Year", "number_of_games_indie": "Number of Games Indie (percentage)", "is_indie": "Is Indie"}
    )
    
    return fig


def camemberg_genres(df, title, color_dict):
    df = df.sort_values("count", ascending=False)

    fig = px.pie(
        df,
        values="count",
        names="genre",
        title=title,
        color="genre", 
        color_discrete_map=color_dict  
    )

    fig.update_traces(sort=False)

    return fig


def parallele_comp(df):
    rating_mapping = {"<60": 0, "60–74": 1, "75–89": 2, "90+": 3}
    df["rating_code"] = df["total_rating"].map(rating_mapping)

    fig = px.parallel_categories(
        df,
        dimensions=["has_reliable_votes", "has_collections", "total_rating", "special", "dlcs"],
        color="rating_code",
        color_continuous_scale=px.colors.sequential.Viridis,
        labels={
            "has_collections": "Collections",
            "special": "Special Type",
            "total_rating": "Total Rating",
            "has_reliable_votes": "Reliable Votes",
            "dlcs": "Number of DLCs"
        }
    )

    fig.update_layout(
        title="Parallel Comparison of Games",
        font=dict(size=20),
        plot_bgcolor='black',
        width=1000,
        height=600,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    df.drop(columns="rating_code", inplace=True)
    return fig