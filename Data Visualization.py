#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

# Load the dataset
file_path = 'path_to_covid_data.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
data.head()


# In[3]:


# Reshape the data from wide format to long format
data_long = data.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], 
                      var_name='Date', value_name='Cases')

# Convert 'Date' column to datetime format
data_long['Date'] = pd.to_datetime(data_long['Date'])

# Sort data by country and date
data_long = data_long.sort_values(['Country/Region', 'Date'])

# Calculate daily new cases by country
data_long['Daily Cases'] = data_long.groupby('Country/Region')['Cases'].diff().fillna(0)

# Display the first few rows of the reshaped and cleaned data
data_long.head()


# In[7]:


# Install the necessary libraries
get_ipython().system('pip install dash plotly')

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Example data
data = {
    'Country/Region': ['Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan'],
    'Date': ['2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26'],
    'Daily Cases': [0, 0, 0, 0, 0]
}
data_long = pd.DataFrame(data)
data_long['Date'] = pd.to_datetime(data_long['Date'])

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("COVID-19 Dashboard"),
    dcc.Dropdown(
        id='country-selector',
        options=[{'label': country, 'value': country} for country in data_long['Country/Region'].unique()],
        value='Afghanistan',
        multi=False
    ),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=data_long['Date'].min(),
        end_date=data_long['Date'].max(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='cases-trend')
])

# Callback to update the graph based on the selected country and date range
@app.callback(
    Output('cases-trend', 'figure'),
    [Input('country-selector', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(selected_country, start_date, end_date):
    filtered_data = data_long[(data_long['Country/Region'] == selected_country) & 
                              (data_long['Date'] >= start_date) & 
                              (data_long['Date'] <= end_date)]
    
    fig = px.line(filtered_data, x='Date', y='Daily Cases', title=f'Daily COVID-19 Cases in {selected_country}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

