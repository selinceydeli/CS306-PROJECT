import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from IPython.display import display, HTML
import folium
import matplotlib.cm as cm
import numpy as np

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Canberk102002',
    'database': 'cs306_project'
}

db_uri = f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}"

# Defining an engine and forming a connection to our MySQL database using this engine
try:
    engine = create_engine(db_uri)
    connection = engine.connect()
except Exception as err:
    print(err)

# Importing the views we created in the previous step of the project
if connection is not None:
    views = [
        "low_democratized_countries",
        "high_schooling_countries",
        "high_development_countries",
        "high_corr_per_countries",
        "high_bribery_countries",
        "high_democratized_countries",
        "low_corr_per_countries"
    ]
    
    dataframes = {}
    
    for view in views:
        query = f"SELECT * FROM {view};"
        dataframes[view] = pd.read_sql(query, connection)

# VISUALIZATIONS

# VISUAL 1
# Low Democratized Countries View - Visualized with a Vertical Column Chart
ax = sns.barplot(data=dataframes["low_democratized_countries"], x="country", y="avg_liberal_dem_idx")
ax.set_xlabel("Country")
ax.set_ylabel("Avg Liberal Democracy Index")
ax.set_title("Low Democratized Countries")
plt.xticks(rotation=90, fontsize=8) # The x-axis labels are rotated 90 degrees and
                                    # font size is adjusted to 8 to prevent the overlapping of the labels
plt.show()

# VISUAL 1 - SECOND VERSION
# Low Democratized Countries View - Visualized with a Vertical Column Chart having "avg_liberal_dem_idx" values ordered

# Sorting the dataframe by 'avg_liberal_dem_idx' column
dataframes["low_democratized_countries"] = dataframes["low_democratized_countries"].sort_values('avg_liberal_dem_idx')

ax = sns.barplot(data=dataframes["low_democratized_countries"], x="country", y="avg_liberal_dem_idx")
ax.set_xlabel("Country")
ax.set_ylabel("Avg Liberal Democracy Index")
ax.set_title("Low Democratized Countries")
plt.xticks(rotation=90, fontsize=8) # The x-axis labels are rotated 90 degrees and
                                    # font size is adjusted to 8 to prevent the overlapping of the labels
plt.show()

# --------

# VISUAL 2
# High Schooling Countries View - Visualized with a Line Chart
plt.figure(figsize=(10, 6))
ax = sns.lineplot(data=dataframes["high_schooling_countries"], x="country", y="avg_schooling_idx", marker="o")
ax.set_xlabel("Country")
ax.set_ylabel("Avg Schooling Index")
ax.set_title("High Schooling Countries")
plt.xticks(rotation=90)
plt.show()

# VISUAL 2 - SECOND VERSION
# IMPROVED: High Schooling Countries View - Visualized with a Line Chart having "avg_schooling_idx" values ordered
sorted_data = dataframes["high_schooling_countries"].sort_values(by="avg_schooling_idx")
plt.figure(figsize=(10, 6))
ax = sns.lineplot(data=sorted_data, x="country", y="avg_schooling_idx", marker="o", color="green")
ax.set_xlabel("Country")
ax.set_ylabel("Avg Schooling Index")
ax.set_title("High Schooling Countries")
plt.xticks(rotation=90, fontsize=8) # The x-axis labels are rotated 90 degrees and
                                    # font size is adjusted to 8 to prevent the overlapping of the labels
plt.show()

# VISUAL 2 - THIRD VERSION
# High Schooling Countries View & Corruption Perception Describes Table - Visualized with a Line Chart

# Importing and processing the data from the Corruption Perception Describes Table
corr_perception_df = pd.read_sql_query("SELECT * FROM CorrupPercep_Describes", connection)
merged_df = pd.merge(dataframes["high_schooling_countries"], corr_perception_df, left_on='country', right_on='iso_code', how='inner')

# Plotting the line chart
plt.figure(figsize=(10, 6))
ax = sns.lineplot(data=merged_df, x="country", y="avg_schooling_idx", marker="o", label="Avg Schooling Index")
sns.lineplot(data=merged_df, x="country", y="corr_per_index", marker="o", color="red", label="Corruption Perception Index")
ax.set_xlabel("Country")
ax.set_ylabel("Index")
ax.set_title("High Schooling Countries and Corruption Perception Index Relationship")
plt.xticks(rotation=90)
plt.legend()
plt.show()

# VISUAL 2 - THIRD VERSION IMPROVED
# IMPROVED: High Schooling Countries View & Corruption Perception Describes Table - Visualized with a Line Chart having "avg_schooling_idx" values ordered

# Importing and processing the data from the Corruption Perception Describes Table
corr_perception_df = pd.read_sql_query("SELECT * FROM CorrupPercep_Describes", connection)
merged_df = pd.merge(dataframes["high_schooling_countries"], corr_perception_df, left_on='country', right_on='iso_code', how='inner')

# Sorting the dataframe by 'avg_schooling_idx' column
merged_df = merged_df.sort_values('avg_schooling_idx')

# Plotting the line chart
plt.figure(figsize=(10, 6))
ax = sns.lineplot(data=merged_df, x="country", y="avg_schooling_idx", marker="o", label="Avg Schooling Index")
sns.lineplot(data=merged_df, x="country", y="corr_per_index", marker="o", color="red", label="Corruption Perception Index")
ax.set_xlabel("Country")
ax.set_ylabel("Index")
ax.set_title("High Schooling Countries and Corruption Perception Index Relationship")
plt.xticks(rotation=90)
plt.legend()
plt.show()

# --------

# VISUAL 3
# High Bribery Countries View - Visualized with a Pie Chart
plt.pie(dataframes["high_bribery_countries"]["avg_bribe_payers_index"],
        labels=dataframes["high_bribery_countries"]["country"],
        autopct='%1.1f%%')
plt.title("High Bribery Countries")
plt.xticks(rotation=90)
plt.show()
    
# VISUAL 3 - SECOND VERSION
# IMPROVED: High Bribery Countries View - Visualized with a Doughnut Chart
plt.pie(dataframes["high_bribery_countries"]["avg_bribe_payers_index"],
        labels=dataframes["high_bribery_countries"]["country"],
        autopct='%1.1f%%',
        pctdistance=0.85,
        wedgeprops=dict(width=0.3))
plt.title("High Bribery Countries")
plt.show()

# --------

# VISUAL 4
# High Development Countries View - Visualized with a Scatter Map / Area Map using the world map as background

# Creating a base map centered around the world
m = folium.Map(location=[0, 0], zoom_start=2)

# Extracting data from the high_development_countries dataframe
data = dataframes["high_development_countries"]

countries={
    "ALB": { "name": "Albania", "latitude": 41.1533, "longitude": 20.1683 },
    "ARE": { "name": "United Arab Emirates", "latitude": 23.4241, "longitude": 53.8478 },
    "ARG": { "name": "Argentina", "latitude": -38.4161, "longitude": -63.6167 },
    "ARM": { "name": "Armenia", "latitude": 40.0691, "longitude": 45.0382 },
    "AUS": { "name": "Australia", "latitude": -25.2744, "longitude": 133.7751 },
    "AUT": { "name": "Austria", "latitude": 47.5162, "longitude": 14.5501 },
    "AZE": { "name": "Azerbaijan", "latitude": 40.1431, "longitude": 47.5769 },
    "BEL": { "name": "Belgium", "latitude": 50.5039, "longitude": 4.4699 },
    "BGR": { "name": "Bulgaria", "latitude": 42.7339, "longitude": 25.4858 },
    "BHR": { "name": "Bahrain", "latitude": 26.0667, "longitude": 50.5577 },
    "BHS": { "name": "Bahamas", "latitude": 25.0343, "longitude": -77.3963 },
    "BIH": { "name": "Bosnia and Herzegovina", "latitude": 43.9159, "longitude": 17.6791 },
    "BLR": { "name": "Belarus", "latitude": 53.7098, "longitude": 27.9534 },
    "BRA": { "name": "Brazil", "latitude": -14.2350, "longitude": -51.9253 },
    "BRB": { "name": "Barbados", "latitude": 13.1939, "longitude": -59.5432 },
    "BRN": { "name": "Brunei", "latitude": 4.5353, "longitude": 114.7277 },
    "CAN": { "name": "Canada", "latitude": 56.1304, "longitude": -106.3468 },
    "CHE": { "name": "Switzerland", "latitude": 46.8182, "longitude": 8.2275 },
    "CHL": { "name": "Chile", "latitude": -35.6751, "longitude": -71.5430 },
    "CHN": { "name": "China", "latitude": 35.8617, "longitude": 104.1954 },
    "COL": { "name": "Colombia", "latitude": 4.5709, "longitude": -74.2973 },
    "CRI": { "name": "Costa Rica", "latitude": 9.7489, "longitude": -83.7534 },
    "CUB": { "name": "Cuba", "latitude": 21.5218, "longitude": -77.7812 },
    "CYP": { "name": "Cyprus", "latitude": 35.1264, "longitude": 33.4299 },
    "CZE": { "name": "Czechia", "latitude": 49.8175, "longitude": 15.4730 },
    "DEU": { "name": "Germany", "latitude": 51.1657, "longitude": 10.4515 },
    "DNK": { "name": "Denmark", "latitude": 56.2639, "longitude": 9.5018 },
    "DOM": { "name": "Dominican Republic", "latitude": 18.7357, "longitude": -70.1627 },
    "DZA": { "name": "Algeria", "latitude": 28.0339, "longitude": 1.6596 },
    "ECU": { "name": "Ecuador", "latitude": -1.8312, "longitude": -78.1834 },
    "ESP": { "name": "Spain", "latitude": 40.4637, "longitude": -3.7492 },
    "EST": { "name": "Estonia", "latitude": 58.5953, "longitude": 25.0136 },
    "FIN": { "name": "Finland", "latitude": 61.9241, "longitude": 25.7482 },
    "FRA": { "name": "France", "latitude": 46.6034, "longitude": 1.8883 },
    "GBR": { "name": "United Kingdom", "latitude": 55.3781, "longitude": -3.4360 },
    "GEO": { "name": "Georgia", "latitude": 42.3154, "longitude": 43.3569 },
    "GRC": { "name": "Greece", "latitude": 39.0742, "longitude": 21.8243 },
    "GRD": { "name": "Grenada", "latitude": 12.1165, "longitude": -61.6790 },
    "HKG": { "name": "Hong Kong", "latitude": 22.3193, "longitude": 114.1694 },
    "HRV": { "name": "Croatia", "latitude": 45.1000, "longitude": 15.2000 },
    "HUN": { "name": "Hungary", "latitude": 47.1625, "longitude": 19.5033 },
    "IRL": { "name": "Ireland", "latitude": 53.1424, "longitude": -7.6921 },
    "IRN": { "name": "Iran", "latitude": 32.4279, "longitude": 53.6880 },
    "ISL": { "name": "Iceland", "latitude": 64.9631, "longitude": -19.0208 },
    "ISR": { "name": "Israel", "latitude": 31.0461, "longitude": 34.8516 },
    "ITA": { "name": "Italy", "latitude": 41.8719, "longitude": 12.5674 },
    "JAM": { "name": "Jamaica", "latitude": 18.1096, "longitude": -77.2975 },
    "JOR": { "name": "Jordan", "latitude": 30.5852, "longitude": 36.2384 },
    "JPN": { "name": "Japan", "latitude": 36.2048, "longitude": 138.2529 },
    "KAZ": { "name": "Kazakhstan", "latitude": 48.0196, "longitude": 66.9237 },
    "KOR": { "name": "South Korea", "latitude": 35.9078, "longitude": 127.7669 },
    "KWT": { "name": "Kuwait", "latitude": 29.3117, "longitude": 47.4818 },
    "LBN": { "name": "Lebanon", "latitude": 33.8547, "longitude": 35.8623 },
    "LCA": { "name": "Saint Lucia", "latitude": 13.9094, "longitude": -60.9789 },
    "LKA": { "name": "Sri Lanka", "latitude": 7.8731, "longitude": 80.7718 },
    "LTU": { "name": "Lithuania", "latitude": 55.1694, "longitude": 23.8813 },
    "LUX": { "name": "Luxembourg", "latitude": 49.8153, "longitude": 6.1296 },
    "LVA": { "name": "Latvia", "latitude": 56.8796, "longitude": 24.6032 },
    "MDA": { "name": "Moldova", "latitude": 47.4116, "longitude": 28.3699 },
    "MDV": { "name": "Maldives", "latitude": 3.2028, "longitude": 73.2207 },
    "MEX": { "name": "Mexico", "latitude": 23.6345, "longitude": -102.5528 },
    "MKD": { "name": "North Macedonia", "latitude": 41.6086, "longitude": 21.7453 },
    "MLT": { "name": "Malta", "latitude": 35.9375, "longitude": 14.3754 },
    "MNE": { "name": "Montenegro", "latitude": 42.7087, "longitude": 19.3744 },
    "MNG": { "name": "Mongolia", "latitude": 46.8625, "longitude": 103.8467 },
    "MUS": { "name": "Mauritius", "latitude": -20.3484, "longitude": 57.5522 },
    "MYS": { "name": "Malaysia", "latitude": 4.2105, "longitude": 101.9758 },
    "NLD": { "name": "Netherlands", "latitude": 52.1326, "longitude": 5.2913 },
    "NOR": { "name": "Norway", "latitude": 60.4720, "longitude": 8.4689 },
    "NZL": { "name": "New Zealand", "latitude": -40.9006, "longitude": 174.8860 },
    "OMN": { "name": "Oman", "latitude": 21.5126, "longitude": 55.9233 },
    "PAN": { "name": "Panama", "latitude": 8.5375, "longitude": -80.7821 },
    "PER": { "name": "Peru", "latitude": -9.1900, "longitude": -75.0152 },
    "POL": { "name": "Poland", "latitude": 51.9194, "longitude": 19.1451 },
    "PRT": { "name": "Portugal", "latitude": 39.3999, "longitude": -8.2245 },
    "PRY": { "name": "Paraguay", "latitude": -23.4425, "longitude": -58.4438 },
    "QAT": { "name": "Qatar", "latitude": 25.3548, "longitude": 51.1839 },
    "ROU": { "name": "Romania", "latitude": 45.9432, "longitude": 24.9668 },
    "RUS": { "name": "Russia", "latitude": 61.5240, "longitude": 105.3188 },
    "SAU": { "name": "Saudi Arabia", "latitude": 23.8859, "longitude": 45.0792 },
    "SGP": { "name": "Singapore", "latitude": 1.3521, "longitude": 103.8198 },
    "SRB": { "name": "Serbia", "latitude": 44.0165, "longitude": 21.0059 },
    "SUR": { "name": "Suriname", "latitude": 3.9193, "longitude": -56.0278 },
    "SVK": { "name": "Slovakia", "latitude": 48.6690, "longitude": 19.6990 },
    "SVN": { "name": "Slovenia", "latitude": 46.1512, "longitude": 14.9955 },
    "SWE": { "name": "Sweden", "latitude": 60.1282, "longitude": 18.6435 },
    "SYC": { "name": "Seychelles", "latitude": -4.6796, "longitude": 55.4920 },
    "THA": { "name": "Thailand", "latitude": 15.8700, "longitude": 100.9925 },
    "TKM": { "name": "Turkmenistan", "latitude": 38.9697, "longitude": 59.5563 },
    "TTO": { "name": "Trinidad and Tobago", "latitude": 10.6918, "longitude": -61.2225 },
    "TUN": { "name": "Tunisia", "latitude": 33.8869, "longitude": 9.5375 },
    "TUR": { "name": "Turkey", "latitude": 38.9637, "longitude": 35.2433 },
    "UKR": { "name": "Ukraine", "latitude": 48.3794, "longitude": 31.1656 },
    "URY": { "name": "Uruguay", "latitude": -32.5228, "longitude": -55.7658 },
    "USA": { "name": "United States", "latitude": 37.0902, "longitude": -95.7129 },
    "VCT": { "name": "Saint Vincent and the Grenadines", "latitude": 12.9843, "longitude": -61.2872 },
    "VEN": { "name": "Venezuela", "latitude": 6.4238, "longitude": -66.5897 },
    "ZAF": { "name": "South Africa", "latitude": -30.5595, "longitude": 22.9375 }
}

# Adding the data points as a scatter plot to the world map
for index, row in data.iterrows():
    country = row["country"]
    avg_hum_dev_idx = row["avg_hum_dev_idx"]

    c = countries[country]["name"]
    
    # Getting latitude and longitude information from the above-defined countries dictionary
    lat, lon = countries.get(c, (countries[country]["latitude"], countries[country]["longitude"]))

    # Checking if the coordinates exist for the country
    if lat is not None and lon is not None:
        folium.CircleMarker(
            location=[lat, lon],
            radius=avg_hum_dev_idx * 4,  # Scaling the circle size in the scatter plot according to the value of the avg_hum_dev_idx
            color="blue",
            fill=True,
            fill_color="blue",
            popup=f"{country}: {avg_hum_dev_idx}"
        ).add_to(m)

# Saving the map with an html extension
m.save("high_development_map.html")

# --------

# VISUAL 5
# High Corruption Perception Countries View - Visualized with a Horizontal Bar Plot

# Sorting the dataframe by 'avg_corr_per_idx' in descending order
sorted_df = dataframes["high_corr_per_countries"].sort_values(by="avg_corr_per_idx", ascending=True)

# Creating a color map
color_map = cm.get_cmap('nipy_spectral')
num_of_countries = len(sorted_df)
colors = color_map(np.linspace(0, 1, num_of_countries))

ax = sorted_df.plot.barh(x="country", y="avg_corr_per_idx", legend=False, color=colors, figsize=(15, 15))
ax.set_xlabel("Avg Corruption Perception Index")
ax.set_ylabel("Country")
ax.tick_params(axis='y', labelsize=6) # Decreasing the label font for the y axis to prevent the overlapping
ax.set_title("High Corruption Perception Countries")
plt.show()
