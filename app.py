# importing dependencies 
import pandas as pd 
import plotly.express as px
import dash 
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output

#loading data
df = pd.read_csv('data.csv')

#deploying the app
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])

app.layout = html.Div([ 
    html.Div(html.H1("Cases of Lethal Police Force in the United States", style={'textAlign':'center'})), #adding a header
    html.Br(), #adding a break between the header and the next elements
    dbc.Row( #initiating a new row
        [dbc.Col( #making a new column 
            [html.Div(
                [html.Br(), 
                 html.H4('Select a Race:'), #adding a header for the radio buttons
                 dcc.RadioItems(id = 'radio-race', 
                            options=['All', 'Asian', 'Black', 'Hispanic', 'Native American', 'Native Hawaiian and Pacific Islander', 'White'],
                            value = 'All')])],
                            width={'size':3}, 
                            style={'padding':'23px'}), #adding padding so the radio buttons are not right on the edge
        dbc.Col( #making another column for the map and slider
            [html.Div(
                [dcc.Graph(id = "map-usa"), #adding my map
                 dcc.RangeSlider(id = "map-slider", #adding the range slider
                             min = df['year'].min(axis = 0), #minimum value is min in df
                             max = df['year'].max(axis = 0), #maximum value is the max in df
                             step = 1, 
                             dots = True,
                             value = [df['year'].min(), df['year'].max()], #setting the range slider value to include all of the years
                             marks = {2012: {'label':'2012', 'style':{'color':'#000000'}}, #making each marker black (every two years
                                      2014:{'label':'2014', 'style':{'color':'#000000'}}, 
                                      2016:{'label':'2016', 'style':{'color':'#000000'}}, 
                                      2018:{'label':'2018', 'style':{'color':'#000000'}}, 
                                      2020:{'label':'2020', 'style':{'color':'#000000'}},  
                                      2022:{'label':'2022', 'style':{'color':'#000000'}}, 
                                      2024:{'label':'2024', 'style':{'color':'#000000'}}},
                             tooltip={"placement": "bottom", "always_visible": True})])], width={'size':9, 'offset':0})]) #making the tooltip for the slider
], className='row')

@app.callback(
    Output('map-usa', 'figure'), 
    Input('map-slider', 'value'), 
    Input('radio-race', 'value'))
def update_graph_date(selected_dates, race):
    filtered_df = df.loc[(df['year'] >= selected_dates[0]) & (df['year'] <= selected_dates[1])] #filtering based on selected dates
    if race != 'All': #filtering if the radio button is not 'all'
        filtered_df = filtered_df[filtered_df['race'].isin([race])]

    fig = px.choropleth(locations=filtered_df['state'].unique(), #using the states from the filtered data above
                     locationmode='USA-states', #setting location mode to the United States
                      color = filtered_df['state'].value_counts(), #having each state be colored by the number of incidents
                       scope = 'usa', #setting the scope of the graph to the US
                        color_continuous_scale="Sunsetdark", #setting color scheme
                        hover_data={'State' : filtered_df['state'].unique(), 'Count ' :filtered_df['state'].value_counts()}) #adding state and count labels
    fig.update_layout(paper_bgcolor='rgba(255,255,255,0.3)') #making the background of the graph slightly transparent
    return fig

if __name__ == '__main__':
    app.run_server(jupyter_mode='tab', debug=True)