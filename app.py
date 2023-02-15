#Load Libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title = "Percentiles Graph",
	page_icon = ":bar_chart:",
	layout = "wide")


##DATA WRANGLING

#Import Data
position_labels_df = pd.read_excel("Dashboard Sheet.xlsx", sheet_name = "Notes", skiprows=25, nrows=7, header=0)
percentiles_df = pd.read_excel("Dashboard Sheet.xlsx", sheet_name = "Percentile Sheet")

#Rename 'percentiles_df['Position Group']' column to 'percentiles_df['Position_Group']'


#Edit Cell from position_labels_df (DM/CM)
position_labels_df['Position Group'][2] = 'CM'


# - - - - SIDEBAR - - - - 
# Sidebar with position group, team and player multiselect
pg = st.sidebar.multiselect("Select a Position Group:", options=percentiles_df['Position Group'].unique())
team = st.sidebar.multiselect("Select a Team:", options=percentiles_df['Team'].unique())

player = st.sidebar.multiselect(
	"Select a player:",
	options = percentiles_df[(percentiles_df['Position Group'].isin(pg)) & (percentiles_df['Team'].isin(team))]['Player'].unique()
)

if len(player) > 0:
	filtered_df = percentiles_df[(percentiles_df['Position Group'].isin(pg)) & (percentiles_df['Team'].isin(team)) & (percentiles_df['Player'].isin(player))]
	filtered_df2 = percentiles_df[(percentiles_df['Position Group'].isin(pg)) & (percentiles_df['Team'].isin(team))]
	st.write(filtered_df2)
	st.write(filtered_df)

	player = filtered_df['Player'].values[0]
	position = filtered_df['Position Group'].values[0]
	percentiles = position_labels_df[position_labels_df['Position Group'] == position].columns[1:]
	percentile_values = filtered_df[percentiles].values[0]
	percentile_labels = position_labels_df.loc[position_labels_df['Position Group'] == position, percentiles].values[0]

	fig, ax = plt.subplots()
	color_codes = ['red' if x <= 0.250 else 'orange' if x <= 0.500 else 'yellow' if x <= 0.750 else 'green' for x in percentile_values]
	ax.barh(percentile_labels, percentile_values, color=color_codes)
	ax.set_xlabel('Percentile')
	ax.set_ylabel('Performance Metrics')
	player_position = filtered_df['Position Group'].values[0]
	ax.set_title(f'Percentiles for {player}, {player_position}')
	st.pyplot()


st.set_option('deprecation.showPyplotGlobalUse', False)
