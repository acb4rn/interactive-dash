# importing dependencies 
import pandas as pd 
import plotly.express as px
import dash 
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, dash_table
import base64


#load dataset
df = pd.read_csv('data.csv')

#creating new df for the datatable 
new_df = df[['name', 'age', 'gender', 'race', 'date', 'city', 'state', 'agency_responsible']]


#initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])

server = app.server 

#loading encoding for the github image 
test_png = 'github-mark-white.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

#creating app 
app.layout = html.Div([ 
    html.Div([html.Br(), #header div
              dbc.Row([
                  dbc.Col(html.H1("Cases of Lethal Police Force in the United States", #title 
                               style={'textAlign':'center', 'fontWeight':'bold', 'color':'white'}), width = {'size':11} ), 
                  dbc.Col(html.A(html.Img(src='data:image/png;base64,{}'.format(test_base64), style = {'height':'60%', 'width':'50%'}), #github img link 
                         href='https://github.com/acb4rn/interactive-dash'),),
    ]),
              html.Br()], style = {'background-color':'#283D3B'}), #changing background color 
    html.Br(), #adding a break between the header and the next elements
    dbc.Row( #initiating a new row
        [dbc.Col( #making another column for the map and slider
            [html.Div(
                [html.H2('Map of Lethal Police Force Cases Between 2012 and 2024',style = {'padding-left':'35px', 'fontWeight':'bold'}), #map title
                html.Br(),
                dcc.Graph(id = "map-usa"), #adding my map
                 dcc.RangeSlider(id = "map-slider", #adding the range slider
                             min = df['year'].min(axis = 0), #minimum value is min in df
                             max = df['year'].max(axis = 0), #maximum value is the max in df
                             step = 1, 
                             dots = True,
                             value = [df['year'].min(), df['year'].max()], #setting the range slider value to include all of the years
                             marks = {2012: {'label':'2012', 'style':{'color':'#495867'}}, #making each marker black (every two years)
                                      2014:{'label':'2014', 'style':{'color':'#495867'}}, 
                                      2016:{'label':'2016', 'style':{'color':'#495867'}}, 
                                      2018:{'label':'2018', 'style':{'color':'#495867'}}, 
                                      2020:{'label':'2020', 'style':{'color':'#495867'}},  
                                      2022:{'label':'2022', 'style':{'color':'#495867'}}, 
                                      2024:{'label':'2024', 'style':{'color':'#495867'}}},
                             tooltip={"placement": "bottom", "always_visible": True})])], width={'size':9, 'offset':0}), #making the tooltip for the slider
            dbc.Col( #making a new column 
            [html.Div(
                [html.H5('About this Project', style = {'color':'#5C1A1B', 'text-align':'center'}), #adding a section describing this dashboard
                 html.P('This dashboard uses data of lethal police force in the United States collected by Mapping Police Violence. The goal of this dashboard is to assist advocates for raising awareness of the degree of lethal police force through a palatable format.Community members can view the number of cases of lethal police force that have occurred in their communities and hold police departments accountable for those deaths.', 
                        style= {'color':'#5C1A1B', 'padding-right':'15px','text-align':'justify'}), #changing color and padding for text
                 html.H3('Select a Race:'), #adding a header for the radio buttons
                 dcc.RadioItems(id = 'radio-race', #creating radio buttons linked to the map 
                            options=['All', 'Asian', 'Black', 'Hispanic', 'Native American', 'Native Hawaiian and Pacific Islander', 'White'],
                            value = 'All')])],
                            width={'size':3}
                            ),
        ]),
        dbc.Row(html.Br()), #inserting a blank row
        dbc.Row([html.Br(),
                html.H2('Victim Datatable', style = {'padding-left':'35px', 'fontWeight':'bold'}), #title for datatable section
                html.H6('The datatable below displays the victims of lethal police violence and the agency or agencies responsible for their deaths. Use the dropdowns to select a state and city to see all of the victims from that locale and use the page button if necessary.', #explanation of next section
                        style = {'padding-left':'35px', 'color':'#5C1A1B'}),
                 html.Br(), 
                 dbc.Col(
                 html.H3('Select a State', style = {'padding-left': '25px'})), #title for state dropdown
                 dbc.Col(
                    html.H3('Select a City') #title for city dropdown
                 )]),
        dbc.Row([
            dbc.Col(dcc.Dropdown( #initializing state dropdown
            id = 'state-dropdown', 
            options=[{"label": st, "value": st} for st in new_df['state'].unique()], #setting values from new_df
            value = 'VA', #Virginia as the default
            style = {'color': 'black', 'padding-left':'23px', 'width':'600px' } #adding styling
            )),
            dbc.Col(dcc.Dropdown( #initializing city dropdown
                id = 'city-dropdown', 
                value = 'Charlottesville', #default is Charlottesville
                style = {'color':'#495867', 'width': '600px'}
            ))
        ]),
        dbc.Row(html.Br()),
        dbc.Row([#initiating a new row
            html.Div(dash_table.DataTable(id = 'interactive-table', #initializing datatable element
                                 data = new_df.to_dict('records'), #linking to the callback
                                  columns=[{'id': c, 'name': c} for c in new_df.columns], #setting columns 
                                  style_cell={'textAlign': 'left'}, #all cells aligned left
                                  style_cell_conditional=[{
                                      'if': {'column_id': ['age', 'date']}, #numerical data aligned right
                                        'textAlign': 'right'}
                                        ], 
                                    style_data={'whiteSpace': 'normal', 
                                                'height': 'auto', #adjusts to the amount of data in cell
                                                'color':'black' 
                                                }, 
                                    style_data_conditional=[{
                                    'if': {'row_index': 'odd'}, #adding striping for easier reading
                                    'backgroundColor': 'rgba(25, 112, 119, 0.3)'}],
                                page_action = 'native', #adding pagination to table 
                                page_current = 0, 
                                page_size = 12, #max number of rows on each page
                                style_header={'fontWeight': 'bold', #styling the header of the table
                                              'color':'white', 
                                              'backgroundColor': '#197278'}
                                ), style = {'padding-left': '35px', 'padding-right':'35px'}) #adding padding for the entire table
            ]), 
        dbc.Row(html.Br()),
        dbc.Row([html.H2('Demographic Distributions', style = {'padding-left':'35px', 'fontWeight':'bold'}), #header for next section
            dbc.Col(dcc.Graph(figure = px.histogram(df, x="race", pattern_shape = 'race', title = 'Race Distribution', #creating race bar chart
                color_discrete_sequence = ['#AF7595']).update_layout(xaxis_title = "Victim's Race", yaxis_title = "Number of Cases", 
                showlegend = False, paper_bgcolor = 'rgba(255,255,255,0.4)', plot_bgcolor = 'rgba(255, 255, 255, 0.7)')
                ),style = {'padding-left':'35px'} 
                ), 
            dbc.Col(dcc.Graph(figure = px.histogram(df, x = 'age', title = 'Distribution of Age', nbins = 40, #age histogram
                color_discrete_sequence = ['#AF7595']).update_layout(xaxis_title = "Victim's Age", yaxis_title = "Number of Cases",
                paper_bgcolor = 'rgba(255, 255,255,0.4)', plot_bgcolor ='rgba(255, 255, 255, 0.7)'), style = {'padding-right':'25px'})
                    ), 
            html.P('Dashboard by Autumn Boaz', style = {'padding':'35px'}) #adding a final signature for my dashboard
        ])
], style = {'background-color':'#EDDDD4'}) #change background color for the entire dashboard

@app.callback( #map callback
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
                        color_continuous_scale="Teal", #setting color scheme
                        hover_data={'State' : filtered_df['state'].unique(), 'Count ' :filtered_df['state'].value_counts()}) #adding state and count labels
    fig.update_layout(paper_bgcolor='#EDDDD4', geo_bgcolor = '#EDDDD4', 
                      autosize = False, 
                      margin = dict(l=0, r=0, b=0, t=0, pad=4, autoexpand=True)) #making the background of the graph slightly transparent
    return fig


@app.callback(#city dropdown callback
    Output('city-dropdown', 'options'), 
    Input('state-dropdown', 'value'))
def set_city_options(chosen_state): 
    state_df = new_df[new_df['state'] == chosen_state] #filtering the dataframe based on selected state
    city_list = state_df['city'].unique().tolist() #each city in the state df to a list format for filtering the city dropdown
    return city_list

@app.callback( #setting city dropdown to filter the datatable
    Output('interactive-table', 'data'),
    Input('state-dropdown', 'value'), 
    Input('city-dropdown', 'value'))
def table_city(chosen_state, chosen_city): 
    dff = new_df[new_df.state.isin([chosen_state])] #new dataframe for the datatable 
    dfff = dff[dff.city.isin([chosen_city])]
    return dfff.to_dict('records') #returns to datatable object in app layout



if __name__ == '__main__':
    app.run_server(debug=True)
