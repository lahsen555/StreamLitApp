import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

# now we fetch some uber data 
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data # we don't want to load all the data each time, so this will prevent that 
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# now displaying our data 
# st.subheader('Raw data')
# st.write(data)

# we can replace the last two lines with this 
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# a header for the plot 
st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

# now let us draw a map 
# st.subheader('Map of all pickups')

# # the problem with this is that the data have to contain the lat and long vars 
# st.map(data)

# you can use this to filter for an our, or whatever you want
hour_to_filter = hour_to_filter = st.slider('hour', 0, 23, 17) # this is another way to filter 
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)