# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize dash app
app = dash.Dash(__name__)

# ------------------------------------------------------
# ---------------------- LAYOUT -------------------------
# ------------------------------------------------------

app.layout = html.Div(children=[
    
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center',
                   'color': '#503D36',
                   'font-size': 40}),
    
    # -------- TASK 1 DROPDOWN -------- #
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # -------- TASK 2 PIE CHART -------- #
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),
    html.P("Payload range (Kg):"),

    # -------- TASK 3 RANGE SLIDER -------- #
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000',
               7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # -------- TASK 4 SCATTER CHART -------- #
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# ------------------------------------------------------
# ---------------------- CALLBACKS ----------------------
# ------------------------------------------------------

# TASK 2: PIE CHART CALLBACK
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):

    df = spacex_df

    # If ALL sites selected → show total success count per site
    if selected_site == 'ALL':
        fig = px.pie(df,
                     values='class',
                     names='LaunchSite',
                     title='Total Successful Launches by Site')
        return fig

    # Otherwise filter the dataframe by the chosen site
    df_site = df[df['LaunchSite'] == selected_site]

    fig = px.pie(df_site,
                 names='class',
                 title=f'Success vs Failure for site {selected_site}')
    return fig


# TASK 4: SCATTER CHART CALLBACK
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):

    low, high = payload_range

    # Filter payload range
    df_filtered = spacex_df[
        (spacex_df['PayloadMass'] >= low) &
        (spacex_df['PayloadMass'] <= high)
    ]

    # If ALL sites selected
    if selected_site == 'ALL':
        fig = px.scatter(
            df_filtered,
            x='PayloadMass',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Outcome for All Sites'
        )
        return fig

    # Filter to a specific site
    df_site = df_filtered[df_filtered['LaunchSite'] == selected_site]

    fig = px.scatter(
        df_site,
        x='PayloadMass',
        y='class',
        color='Booster Version Category',
        title=f'Payload vs. Outcome for site {selected_site}'
    )
    return fig


# ------------------------------------------------------
# ---------------------- RUN APP -----------------------
# ------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)