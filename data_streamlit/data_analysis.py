import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


df = pd.read_csv('../assets/police.csv')

st.title("Police Crime Dashboard")

# Total crimes
total = len(df)
st.write(f"Total antal forbrydelser: {total}")

# Categories
crimes_per_category = df["Incident Category"].value_counts()

st.subheader("Crimes per category")
fig1, ax1 = plt.subplots()
ax1.bar(crimes_per_category.index, crimes_per_category.values)
plt.xticks(rotation=90)
st.pyplot(fig1)

# Crimes per year
crimes_per_year = df["Incident Year"].value_counts().sort_index()

st.subheader("Crimes per year")
st.write(f"År med flest forbrydelser: {crimes_per_year.idxmax()}")
st.write(f"År med færreste forbrydelser: {crimes_per_year.idxmin()}")

fig2, ax2 = plt.subplots()
ax2.bar(crimes_per_year.index, crimes_per_year.values)
st.pyplot(fig2)