import streamlit as st
import pandas as pd

# --- CONGIS ---
DATA_FILE = "Fantasy.csv"
DATA_FILE_2 = "Fantasy.xlsx"

# --- PAGE SETUP ---
st.set_page_config(page_title="Super Duper League", page_icon="📊")
st.title("Fantasy Super Duper League")

st.subheader("Data")

# --- LOAD DATA ---
data = pd.read_excel(DATA_FILE_2)
st.dataframe(data)

# Get unique captains and their counts
captain_counts = data["Captain"].value_counts()

# Create a DataFrame for captain appearances
captain_df = pd.DataFrame({
    "Captain": captain_counts.index,
    "Appearances": captain_counts.values
})

# Aggregate the points from the "PointsCaptainHalf" and "Kolonne3" columns using groupby
agg_points_half = data.groupby("Captain")["PointsCaptainHalf"].sum().reset_index()
agg_kolonne3 = data.groupby("Captain")["Kolonne3"].sum().reset_index()

# Merge the aggregated data into the captain_df
captain_df = captain_df.merge(agg_points_half, on="Captain", how="left")
captain_df = captain_df.merge(agg_kolonne3, on="Captain", how="left")

# Rename the columns for clarity
captain_df.rename(columns={"PointsCaptainHalf": "Points Captain", "Kolonne3": "Tripple Points Captain"}, inplace=True)

# Display the DataFrame with the new columns
st.subheader("Captains, Appearances, and Aggregated Points, All Teams")
st.dataframe(captain_df)

# --- CHART ---
# Set the Captain as the index for easier plotting
captain_df.set_index('Captain', inplace=True)

# Create a bar chart for appearances and aggregated points
st.subheader("Captains' Appearances and Points (double and tripple)")

# You can plot multiple columns together
st.bar_chart(captain_df[['Tripple Points Captain', 'Points Captain']])

# Alternatively, create separate bar charts for each column if needed
# st.bar_chart(captain_df['Appearances'])
# st.bar_chart(captain_df['Points Captain'])
# st.bar_chart(captain_df['Tripple Points Captain'])
