import dash, locale, requests
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from get_fig import Map, get_stack

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

df = pd.read_csv('countries.csv')
countries = [{'label':country[1][-1], 'value':"%s/%s/%s"%(country[1].latitude,country[1].longitude,country[1][-1])} for country in df.iterrows()]
locale.setlocale(locale.LC_NUMERIC, 'en_IN')

fig_obj = Map()

# Create app layout
app.title = 'Covid19'
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Covid 19 Tracker",
                                    style={"margin-bottom": "0px"},
                                ),
                            ]
                        )
                    ],
                    className="column",
                    id="title",
                )
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="confirmed"), html.P("Confirmed")],
                                    id="wells",
                                    className="mini_container",
                                    style={'background-color':'rgba(128,128,128,0.5)'}
                                ),
                                html.Div(
                                    [html.H6(id="active"), html.P("Active")],
                                    id="gas",
                                    className="mini_container",
                                    style={'background-color':'rgba(255,255,0,0.5)'}
                                ),
                                html.Div(
                                    [html.H6(id="recovered"), html.P("Recovered")],
                                    id="oil",
                                    className="mini_container",
                                    style={'background-color':'rgba(0,128,0,0.5)'}
                                ),
                                html.Div(
                                    [html.H6(id="deaths"), html.P("Deaths")],
                                    id="water",
                                    className="mini_container",
                                    style={'background-color':'rgba(255,0,0,0.5)'}
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        )
                    ],
                    id="right-column",
                    className="columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [   html.P("Select the Country to navigate directly"),
                        dcc.Dropdown(
                            id='dropdown',
                            options=countries,
                            value=None
                        )
                ],
                    className="pretty_container four columns"
                ),
            ],
            className="row flex-display"
        ),
        html.Div(
            [
                html.Div(
                        [dcc.Loading(
                            children=dcc.Graph(figure=fig_obj.get_fig(),id="main_graph"),
                            type='dot',
                            fullscreen=True
                    )],
                    className="pretty_container column",
                ),
                html.Div(
                    [dcc.Graph(figure=get_stack('India'),id="individual_graph")],
                    className="pretty_container column",
                ),
            ],
            className="row flex-display",
        ),
        dcc.Interval(
                id='interval-component',
                interval=600000, # in milliseconds 10 minutes
                n_intervals=0
        ),
        # html.P("Data is Updated every 10 minutes", style={"text-align":"right"}),
        html.Div([
            html.Div(
                'Developed by Suraj Deshmukh', className='column',
            ),
            html.Div(
                "Data is Updated every 10 minutes", className='column',style={'text-align': 'right', 'margin-right': '0.5%'}
                )],
            className='row flex-display'
        ),
        # html.Footer(['Developed by Suraj Deshmukh']),
        html.Footer([html.A(html.Img(src=app.get_asset_url("GitHub-Mark-32px.png"), style={'height':'20px', 'width':'auto'}), href='https://github.com/suraj-deshmukh'),
                     ' ',
                     html.A(html.Img(src=app.get_asset_url("LI-In-Bug.png"), style={'height':'20px', 'width':'auto'}), href='https://www.linkedin.com/in/suraj-deshmukh-86245069/'),
                     ' ',
                     html.A(html.Img(src=app.get_asset_url("so-icon.png"), style={'height':'20px', 'width':'auto'}), href='https://stackoverflow.com/users/5876383/suraj-deshmukh')], className='column')
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback([Output('confirmed', 'children'),
               Output('active', 'children'),
               Output('recovered', 'children'),
               Output('deaths', 'children'),
               Output('main_graph', 'figure'),
               Output('individual_graph', 'figure')],
              [Input('interval-component', 'n_intervals'),
               Input('dropdown', 'value')])
def update_metrics(n, value):
    # print('updating.....')
    data = requests.get("https://corona.lmao.ninja/v2/all").json()
    confirmed = locale.format("%d", data['cases'], grouping=True)
    active = locale.format("%d", data['active'], grouping=True)
    recovered = locale.format("%d", data['recovered'], grouping=True)
    deaths = locale.format("%d", data['deaths'], grouping=True)
    fig = fig_obj.update_fig()
    country = 'India' if value is None else value.split('/')[-1]
    lat, lon = [23.173939, 81.56512] if value is None else value.split('/')[:-1]
    print(country, lat, lon)
    fig.update_layout(
            mapbox=dict(
            center=dict(
                lat=float(lat),
                lon=float(lon)
            ),
            pitch=0,
            zoom=4
        )
    )
    return confirmed, active, recovered, deaths, fig, get_stack(country)


# Main
if __name__ == "__main__":
    app.run_server(host='0.0.0.0',port=80,debug=False)
