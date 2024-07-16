from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json
from urllib.request import urlopen
from datetime import datetime
import numpy as np
from sqlalchemy import create_engine
import pandas as pd

# Define MySQL connection parameters
db_user = 'db_userdfdsgfdg'
db_pass = 'db_passfwefewfe'
db_host = '192.168.250.129'
db_name = 'canada_stats'

# Load the geojson data for Canada provinces
with urlopen('https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/canada.geojson') as response:
    canada_geojson = json.load(response)

# Create SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}')
# Initial SQL
sql_init = '''
SELECT A.year, A.homicides, B.location
FROM homicides A
LEFT JOIN (SELECT province as location, sgc_code FROM provinces) B
ON A.sgc_code = B.sgc_code
'''
df = pd.read_sql(sql_init, con=engine)
dict_cat = {'homicides': 'Avg. Homicides',
            'persons_charged': 'Avg. Persons Charged',
            'pct_charged': '% Persons Charged'}
# color_min = df['homicides'].min()
# color_max = df['homicides'].max()

# Create the initial Plotly figure
fig = px.choropleth_mapbox(df, geojson=canada_geojson, locations='location', featureidkey="properties.name", color='homicides',
                           color_continuous_scale="rdbu_r",
                           range_color=(df['homicides'].min(), df['homicides'].max()),  # Adjust range dynamically
                           mapbox_style="carto-positron",
                           zoom=2.5, center={"lat": 59.6868, "lon": -110.2421},
                           opacity=0.5,
                           labels={'homicides': 'Homicides', 'location': 'Province'}
                          )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Create the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Canada Crime Statistics by Province", style={'text-align': 'center'}),

    dcc.RadioItems(
        id='category-selector',
        options = [
                {'label': 'Avg. Homicides', 'value': 'homicides'},
                {'label': 'Avg. Persons Charged', 'value': 'persons_charged'},
                {'label': '% Persons Charged ', 'value': 'pct_charged'}
            ],
        value = 'homicides', 
        style={'text-align': 'center'}),

    dcc.Graph(id="choropleth-map", figure=fig, style={'width': '50%', 'margin': 'auto'}),

    html.Div([
        dcc.RangeSlider(
            id='year-range-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            step=1,
            value=[df['year'].min(), df['year'].max()],
            marks={year: str(year) for year in range(df['year'].min(), df['year'].max() + 1)}
        )
    ], style={'width': '35%', 'margin': 'auto'})


])

# Define callback to update the figure based on year range selection
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('year-range-slider', 'value'),
     Input('category-selector', 'value')]
)
def update_figure(year_range, category):
    
    if category=='pct_charged':
        sql_update = f'''
        SELECT H.year, H.homicides, PC.persons_charged, P.location
        FROM homicides H
        LEFT JOIN persons_charged PC
        ON H.year = PC.year AND H.sgc_code = PC.sgc_code
        LEFT JOIN (SELECT province as location, sgc_code FROM provinces) P
        ON H.sgc_code = P.sgc_code
        '''
        df = pd.read_sql(sql_update, con=engine)
        filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

        avg_data = filtered_df.groupby('location')[['persons_charged','homicides']].sum().reset_index()
        avg_data[category] = (100*avg_data['persons_charged']/avg_data['homicides']).round(2)
        avg_data[category] = np.where(avg_data[category]>100,100,avg_data[category])
        color_scale = "magma"

    else:
        sql_update = f'''
        SELECT A.year, A.{category}, B.location
        FROM {category} A
        LEFT JOIN (SELECT province as location, sgc_code FROM provinces) B
        ON A.sgc_code = B.sgc_code
        '''
        df = pd.read_sql(sql_update, con=engine)
        filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

        avg_data = filtered_df.groupby('location')[category].mean().reset_index()
        avg_data[category] = avg_data[category].round(2)
        color_scale = "rdbu_r" if category=='homicides' else "rdbu"
        
    fig = px.choropleth_mapbox(avg_data, geojson=canada_geojson, locations='location', featureidkey="properties.name", color=category,
                            color_continuous_scale=color_scale,
                            range_color=(avg_data[category].min(), avg_data[category].max()),
                            mapbox_style="carto-positron",
                            zoom=2.3, center={"lat": 61, "lon": -95},
                            opacity=0.5,
                            labels={category: dict_cat[category], 'location': 'Province'}
                            )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)