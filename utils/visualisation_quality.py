## The functions that will be used on the notes.py page, displaying the graphs for the different ratings


# Import the required libraries
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def plot_average_rating(df, excluded_categories=False):
    """
    Displays a barplot of the average game ratings per year.

    Parameters:
    - df: DataFrame with columns ["year", "average_rating", "has_reliable_votes"]
    - excluded_categories: if True, only includes rows with reliable votes (optional)
    """
    # Copy to avoid modifying the original DataFrame
    filtered_df = df.copy()

    # Apply filter if requested
    if excluded_categories:
        filtered_df = filtered_df[filtered_df["has_reliable_votes"] == True]
    else:
        # Compute average across both True & False (i.e. global average)
        filtered_df = (filtered_df.groupby("year")["average_rating"].mean().reset_index())
        filtered_df["has_reliable_votes"] = "All"

    # Calculate the global mean
    global_mean = filtered_df["average_rating"].mean()

    # Set seaborn theme
    fig, ax = plt.subplots(figsize=(14,6))
    sns.set_theme(style="whitegrid")

    # Add a horizontal line at the mean value
    ax.axhline(global_mean, color="red", linestyle="--", linewidth=2, label=f"Global Mean ({global_mean:.1f})")

    # Create the barplot
    sns.barplot(
        data=filtered_df,
        x="year",
        y="average_rating",
        palette="flare",
        ax=ax
    )

    # Add titles and labels
    ax.set_title("Average Game Rating by Release Year", fontsize=16, weight='bold')
    ax.set_xlabel("Release Year", fontsize=12)
    ax.set_ylabel("Average Rating", fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    return fig


def plot_average_rating_collection(df, excluded_categories=False):
    """
    Displays a barplot of the average game ratings per year,
    split by 'has_collections'

    Parameters:
    - df: DataFrame with columns ["year", "average_rating", "has_reliable_votes"]
    - excluded_categories: if True, only includes rows with reliable votes (optional)
    """
    # Copy to avoid modifying the original DataFrame
    filtered_df = df.copy()

    # Apply filter if requested
    if excluded_categories:
        filtered_df = filtered_df[filtered_df["has_reliable_votes"] == True]
    else:
        # Compute average across both True & False 
        filtered_df = filtered_df.groupby(["year", "has_collections"])["average_rating"].mean().reset_index()
        filtered_df["has_reliable_votes"] = "All"

    # Calculate the global mean
    global_mean = filtered_df["average_rating"].mean()

    # Set seaborn theme
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14,6))

    # Colors
    palette = {False: "#4e79a7", True: "#3cc465"} 

    # Barplot
    sns.barplot(
        data=filtered_df,
        x="year",
        y="average_rating",
        hue="has_collections",
        palette=palette,
        ax=ax
    )

    # Horizontal line for global mean
    ax.axhline(global_mean, color="red", linestyle="--", linewidth=2, label=f"Global Mean ({global_mean:.1f})")

    # Titles and labels
    ax.set_title("Average Game Rating by Release Year (by Collection)", fontsize=16, weight='bold')
    ax.set_xlabel("Release Year", fontsize=12)
    ax.set_ylabel("Average Rating", fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    # Legend 
    ax.legend(
        title="Part of a Collection?", 
        title_fontsize=12, 
        fontsize=11, 
        bbox_to_anchor=(1,1),
        frameon=True, 
        framealpha=0.9,
    )

    return fig


def plot_average_rating_genre(df, excluded_categories=False):
    """
    Displays a barplot of the average game ratings per year,
    split by presence of a genre in 'genre_list' (e.g., 'Indie').

    Parameters:
    - df: DataFrame with columns ["year", "average_rating", "has_reliable_votes", "genres"]
    - excluded_categories: if True, only includes rows with reliable votes
    """
    # Copy to avoid modifying the original DataFrame
    filtered_df = df.copy()

    # Apply filter if requested
    if excluded_categories:
        filtered_df = filtered_df[filtered_df["has_reliable_votes"] == True]
    else:
        # Compute average across both True & False 
        filtered_df = filtered_df.groupby(["year", "is_indie"])["average_rating"].mean().reset_index()
        filtered_df["has_reliable_votes"] = "All"

    # Calculate the global mean
    global_mean = filtered_df["average_rating"].mean()

    # Set seaborn theme
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14,6))

    # Colors
    palette = {True: "#924ea7", False: "#553cc4"} 

    # Barplot
    sns.barplot(
        data=filtered_df,
        x="year",
        y="average_rating",
        hue="is_indie",
        palette=palette,
        ax=ax
    )

    # Horizontal line for global mean
    ax.axhline(global_mean, color="red", linestyle="--", linewidth=2, label=f"Global Mean ({global_mean:.1f})")

    # Titles and labels
    ax.set_title("Average Game Rating by Release Year (by Indie)", fontsize=16, weight='bold')
    ax.set_xlabel("Release Year", fontsize=12)
    ax.set_ylabel("Average Rating", fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    # Legend 
    ax.legend(
        title="Is an Indie?", 
        title_fontsize=12, 
        fontsize=11, 
        bbox_to_anchor=(1,1),
        frameon=True, 
        framealpha=0.9,
    )

    return fig


def plot_average_rating_companies_exclu(df, name, excluded_categories=False):
    """
    Displays a barplot of the average game ratings per year,
    split by presence of a name in 'platform_family' 

    Parameters:
    - df: DataFrame 
    - name: name of companies
    - excluded_categories: if True, only includes rows with reliable votes
    """
    # Copy to avoid modifying the original DataFrame
    filtered_df = df.copy()

    # Apply filter if requested
    if excluded_categories:
        filtered_df = filtered_df[filtered_df["has_reliable_votes"] == True]
    else:
        # Compute average across both True & False
        filtered_df = filtered_df.groupby(["year", "is_exclu"])["average_rating"].mean().reset_index()
        filtered_df["has_reliable_votes"] = "All"
    
    # Calculate the global mean
    global_mean = filtered_df["average_rating"].mean()

    # Set seaborn theme
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14,6))

    # Colors
    palettes = {
        "Nintendo": {True: "#E60012", False: "#FF6666"},     
        "PlayStation": {True: "#003087", False: "#4F83CC"},  
        "Xbox": {True: "#107C10", False: "#5BC74B"},        
        "Windows": {True: "#0078D7", False: "#6EC1E4"},     
        "Apple": {True: "#999999", False: "#CCCCCC"},        
        "Linux": {True: "#000000", False: "#666666"},        
        "Sega": {True: "#004C97", False: "#5B9BD5"},         
        "Smart TV": {True: "#FF9900", False: "#FFCC66"}    
    }

    # Barplot
    sns.barplot(
        data=filtered_df,
        x="year",
        y="average_rating",
        hue="is_exclu",
        palette=palettes[name],
        ax=ax
    )

    ax.axhline(global_mean, color="red", linestyle="--", linewidth=2, label=f"Global Mean ({global_mean:.1f})")

    # Titles and labels
    ax.set_title(f"Average Game Rating by Release Year for {name} (by Exclusivity)", fontsize=16, weight='bold')
    ax.set_xlabel("Release Year", fontsize=12)
    ax.set_ylabel("Average Rating", fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    # Legend 
    ax.legend(
        title="Is an Exclu?", 
        title_fontsize=12, 
        fontsize=11, 
        bbox_to_anchor=(1,1),
        frameon=True, 
        framealpha=0.9,
    )

    return fig


def plot_top10(df, palette, excluded_categories=False):
    # Copy to avoid modifying the original DataFrame
    filtered_df = df.copy()

    # Apply filter if requested
    if excluded_categories:
        filtered_df = filtered_df[filtered_df["has_reliable_votes"] == True]
    else:
        # Compute average across both True & False
        filtered_df["has_reliable_votes"] = "All"

    filtered_df = filtered_df.head(15)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14,6))

    sns.barplot(
        data=filtered_df,
        x="total_rating",
        y="name",
        ax=ax,
        palette=palette
    )

    if palette == "flare":
        title = "Top 15 (in collection)"
    elif palette == "crest":
        title = "Top 15 (no collection)"
    elif palette == "magma":
        title = "Top 15 (only Indie)"
    else:
        title = "Top 15 (only Exclusivity)"
    
    ax.set_title(title, fontsize=16, weight='bold')
    ax.set_xlabel("Average Rating", fontsize=12)
    ax.set_ylabel("Name", fontsize=12)

    for i, v in enumerate(filtered_df["total_rating"]):
        ax.text(v + 0.2, i, f"{v:.1f}", color='black', va='center', fontsize=10)

    return fig


def camembert_grouped(df, number, category_key, category_map, label_map=None, excluded_categories=False):
    """
    Displays a pie chart for a group of boolean columns using Plotly Express:
    - 'has_collections' -> True / False
    - 'game_modes' -> single / multi / both / other
    - 'age_ratings' -> everyone / child / teen / young / 18+
    
    Colors are mapped explicitly for clarity.
    """

    filtered_df = df.copy()
    if excluded_categories:
        filtered_df = filtered_df[filtered_df["has_reliable_votes"] == True]

    filtered_df = filtered_df.head(number)
    columns = category_map[category_key]

    values = []
    labels = []

    if category_key == "has_collections":
        val_true = filtered_df["has_collections"].mean() * 100
        val_false = 100 - val_true
        values = [val_true, val_false]
        labels = [
            f"{label_map[columns[0]] if label_map else columns[0]} True",
            f"{label_map[columns[0]] if label_map else columns[0]} False"
        ]
        colors = ['#4e79a7', '#f28e2b']
    else:
        for col in columns:
            val = filtered_df[col].mean() * 100
            values.append(val)
            labels.append(label_map[col] if label_map and col in label_map else col)
        # Use a color palette
        colors = px.colors.qualitative.Set3[:len(values)]

    # Create Plotly Express pie chart
    fig = px.pie(
        names=labels,
        values=values,
        color=labels,
        color_discrete_sequence=colors,
        title=f"{category_key.replace('_',' ').title()} - Top {number}"
    )

    fig.update_traces(textinfo='percent+label', textfont_size=12, marker=dict(line=dict(color='white', width=1)))
    fig.update_layout(title_font_size=16, title_font_family="Arial", legend_title_text=category_key.replace("_"," ").title())
    
    return fig