
# 🎮 Video Games Data Storytelling (2000–2025)

## Description

This project is an **interactive exploration of video game evolution** from 2000 to 2025, based on public data from the **IGDB (Internet Games Database)**.  
It combines **quantitative analysis, interactive visualizations, and storytelling** to highlight:

- The evolution of the **number of games released** and the **growth of indie games**.
- The **global distribution of developers and publishers**.
- The **distribution of genres and platforms**.
- Correlations between **game quality (ratings) and quantity**, game types, and DLCs.

This project is intended for **educational and analytical purposes**, emphasizing **data storytelling** and **methodological transparency**.

---

## Project Structure

StreamlitApp25/  
├── creation_data_API.py # Script to collect and preprocess raw data from IGDB  
├── project/   
│ ├── app.py # Main Streamlit app entry point   
│ ├── sections/ # Different pages of the Streamlit app   
│ │ ├── home.py # Homepage with project introduction   
│ │ ├── quantity.py # Analysis quantity  
│ │ ├── notes.py # Analysis quality     
│ │ ├── map.py # Shows developers/publishers by country    
│ │ ├── conclusion.py # Project conclusions and future perspectives   
│ ├── data/ # Data storage and preprocessing   
│ │ ├── data.csv # Raw data retrieved from the IGDB API   
│ │ ├── games.csv # Cleaned and preprocessed data ready for analysis   
│ │ └── preparation.ipynb # Jupyter Notebook used to clean and prepare the data   
│ ├── utils/ # Utility scripts   
│ │ ├── io.py # load data   
│ │ ├── visualisation_quantity.py # Functions for plotting quantity-related visualizations    
│ │ ├── visualisation_quality.py # Functions for plotting quality-related visualizations   
│ │ └── visualisation_map.py # Functions for plotting maps and category visualizations   
│ ├── assets/ # UI assets for the Streamlit app    
│ │ ├── light/ # Light mode images/icons     
│ │ └── dark/ # Dark mode images/icons     
│ └── requirements.txt # Python dependencies     


---

## Technologies Used

- **Python 3.10+**
- **Streamlit** for interactive web apps
- **Plotly** for interactive visualizations
- **Pandas & NumPy** for data processing
- **Ast** for parsing list columns
- **PyCountry** for ISO country codes

---

## How to Run
- pip install -r requirements.txt
- streamlit run app.py

---

## Online link 
https://ramdjee-streamlitapp25-20240327-hassane-ramdjee-dai-app-5s3mk6.streamlit.app/


