import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


@st.cache_data
def load_data():
    return pd.read_csv('assets/police.csv')

df = load_data()

st.title("Police Crime Dashboard")

# Total crimes
total = len(df)
st.write(f"Total antal forbrydelser: {total}")

# Categories
crimes_per_category = df["Incident Category"].value_counts()
# Crimes per year
crimes_per_year = df["Incident Year"].value_counts().sort_index()

category_options = ["Select category"] + list(df["Incident Category"].unique())
year_options = ["Select year"] + sorted(df["Incident Year"].unique())

#Laver dropdown i sidebar
category_dropdown = st.sidebar.selectbox("Select Crime Category", category_options)
year_dropdown = st.sidebar.selectbox("Select Year", year_options)

#Starter med det fulde dataframe
filtered_df = df.copy()

if category_dropdown != "Select category":
    filtered_df = filtered_df[filtered_df["Incident Category"] == category_dropdown]

if year_dropdown != "Select year":
    filtered_df = filtered_df[filtered_df["Incident Year"] == year_dropdown]



fig, ax = plt.subplots(figsize=(10, 5))

if category_dropdown != "Select category":
    crimes_per_subcategory = filtered_df["Incident Subcategory"].value_counts()
    crimes_per_subcategory.plot(kind="bar", ax=ax)
    ax.set_title(f"Crime Count: {category_dropdown} ({year_dropdown if year_dropdown != 'Select year' else 'All years'})")
    ax.set_xlabel("Crime subcategory")
else:
    crimes_per_category = filtered_df["Incident Category"].value_counts()
    crimes_per_category.plot(kind="bar", ax=ax)
    ax.set_title("Crimes per category")
    ax.set_xlabel("Category")    


ax.set_ylabel("Number of Crimes")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

#Viser kun data hvis der er valgt noget
with st.expander("Raw data", expanded=True):
    if category_dropdown != "Select category" or year_dropdown != "Select year":
        st.write(filtered_df)
    else:
        st.write("Please select a category or year")



map_df = filtered_df.rename(columns={
    "Latitude": "lat",
    "Longitude": "lon"
})

#Koordinaterne bruger komma i stedet for punktion, derfor skal man replace
map_df["lat"] = pd.to_numeric(map_df["lat"].str.replace(",", "."), errors="coerce")
map_df["lon"] = pd.to_numeric(map_df["lon"].str.replace(",", "."), errors="coerce")

st.map(map_df[["lat", "lon"]].dropna())