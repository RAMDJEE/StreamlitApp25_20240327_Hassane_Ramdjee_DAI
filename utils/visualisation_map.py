## The functions that will be used on the map.py page

import numpy as np

# Import the required libraries
import plotly.express as px


def map_general(df, title):

    fig = px.choropleth(
        df,
        locations="iso_alpha",   
        color="total",           
        color_continuous_scale="Blues",  
        projection="natural earth",
        hover_data={
            "developer": True,
            "publisher": True,
            "total": False  
        },
        title=title,
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Number of games"
        )
    )

    return fig

def map_general_year(df, title):

    fig = px.choropleth(
        df,
        locations="iso_alpha",   
        color="total",           
        color_continuous_scale="Blues",  
        projection="natural earth",
        hover_data={
            "developer": True,
            "publisher": True,
            "total": False  
        },
        animation_frame="year",
        title=title,
    )

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Number of games"
        )
    )

    return fig

def camemberg(df,categories):
    fig = px.pie(
        df,
        values="count",
        names=categories,
        color=categories
    )

    return fig