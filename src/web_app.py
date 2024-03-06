import dash
from dash import Dash, dcc, html, dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash import Dash, html, Input, Output, State
#import dash_player as dp
import dash_player

# update the web app (not API) so that it takes in multiple artist inputs



app = Dash(__name__)

def query(artists: list, n: int) -> list:
    if artists:
        return ['Drake'] * n  # Example output
    else:
        raise ValueError('No artists provided.')

app.layout = html.Div([
    # Header section
    html.Div(
        [html.H1('Discover Your Rhythm', className='custom-header'),
         html.H2('Where you can discover new artists both near and far!', className='subtitle-header')],
        className='header-container'
    ),

    # input section for artist recommendations/searches
    dcc.Input(id='artist-input', type='text', placeholder='Enter artists you like separated by comma', className='artist-input'),
    html.Button('Submit', id='submit-val', n_clicks=0, className='submit-button'),
    html.Div(id='recommendation-output', className='recommendation-output'),

    # Leaving everything above untouched in case this doesn't work. Below is the music dash_player

    html.Div(
            [
                html.Div(
                    style={"width": "48%", "padding": "0px"},
                    children=[
                        dash_player.DashPlayer(
                            id="player",
                            url="https://youtu.be/xpVfcZ0ZcFM?si=-M8l8vkZcKh8jXJc",
                            controls=True,
                            width="100%",
                            height="250px",
                        ),
                        dcc.Checklist(
                            id="bool-props-radio",
                            options=[
                                {"label": val.capitalize(), "value": val}
                                for val in [
                                    "playing",
                                    "loop",
                                    "controls",
                                    "muted",
                                ]
                            ],
                            value=["controls"],
                            inline=True,
                            style={"margin": "20px 0px"},
                        ),
                        html.Div(
                            [
                                dcc.Input(
                                    id="seekto-number-input",
                                    type="number",
                                    placeholder="seekTo value",
                                    style={"width": "calc(100% - 115px)"},
                                ),
                                html.Button(
                                    "seekTo",
                                    id="seekto-number-btn",
                                    style={"width": "105px"},
                                ),
                            ],
                            style={"margin": "20px 0px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    id="current-time-div",
                                    style={"margin": "10px 0px"},
                                ),
                                html.Div(
                                    id="seconds-loaded-div",
                                    style={"margin": "10px 0px"},
                                ),
                                html.Div(
                                    id="duration-div",
                                    style={"margin": "10px 0px"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                            },
                        ),
                    ],
                ),
                html.Div(
                    style={"width": "48%", "padding": "10px"},
                    children=[
                        html.P("Volume:", style={"marginTop": "30px"}),
                        dcc.Slider(
                            id="volume-slider",
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode="drag",
                            marks={0: "0%", 0.5: "50%", 1: "100%"},
                        ),
                        html.P("Playback Rate:", style={"marginTop": "25px"}),
                        dcc.Slider(
                            id="playback-rate-slider",
                            min=0,
                            max=2,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) + "x" for i in [0, 0.5, 1, 1.5, 2]},
                            value=1,
                        ),
                        html.P(
                            "Update Interval for Current Time:",
                            style={"marginTop": "30px"},
                        ),
                        dcc.Slider(
                            id="intervalCurrentTime-slider",
                            min=0,
                            max=1000,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) for i in [0, 250, 500, 750, 1000]},
                            value=250,
                        ),
                        html.P(
                            "Update Interval for Seconds Loaded:",
                            style={"marginTop": "30px"},
                        ),
                        dcc.Slider(
                            id="intervalSecondsLoaded-slider",
                            min=0,
                            max=1000,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) for i in [0, 250, 500, 750, 1000]},
                            value=500,
                        ),
                        html.P(
                            "Update Interval for Duration:",
                            style={"marginTop": "30px"},
                        ),
                        dcc.Slider(
                            id="intervalDuration-slider",
                            min=0,
                            max=1000,
                            step=None,
                            updatemode="drag",
                            marks={i: str(i) for i in [0, 250, 500, 750, 1000]},
                            value=500,
                        ),
                    ],
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "justifyContent": "space-between",
            },
        ),


])

#Leave the portition below untouched

@app.callback(
    Output('recommendation-output', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('artist-input', 'value')]  # Ensure state is imported and used correctly
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        artists = [artist.strip() for artist in value.split(',')] if value else []
        recommended_artists = query(artists, 5)  # Top 5 recommendations
        return html.Ul([html.Li(artist) for artist in recommended_artists])
    return 'Enter artists and click submit to get recommendations.'


# Leave this portion untouched^^

# Need to check with team how much we care about the actual video playback stuff

@app.callback(
    Output("player", "playing"),
    Output("player", "loop"),
    Output("player", "controls"),
    Output("player", "muted"),
    Input("bool-props-radio", "value"),
)
def update_bool_props(values):
    playing = "playing" in values
    loop = "loop" in values
    controls = "controls" in values
    muted = "muted" in values
    return playing, loop, controls, muted


@app.callback(
    Output("player", "seekTo"),
    Input("seekto-number-btn", "n_clicks"),
    State("seekto-number-input", "value"),
)
def set_prop_seekTo(n_clicks, seekto):
    return seekto


@app.callback(
    Output("current-time-div", "children"),
    Input("player", "currentTime"),
)
def display_currentTime(currentTime):
    return f"Current Time: {currentTime}"


@app.callback(
    Output("seconds-loaded-div", "children"),
    Input("player", "secondsLoaded"),
)
def display_secondsLoaded(secondsLoaded):
    return f"Second Loaded: {secondsLoaded}"


@app.callback(
    Output("duration-div", "children"),
    Input("player", "duration"),
)
def display_duration(duration):
    return f"Duration: {duration}"


@app.callback(
    Output("player", "volume"),
    Input("volume-slider", "value"),
)
def set_volume(value):
    return value


@app.callback(
    Output("player", "playbackRate"),
    Input("playback-rate-slider", "value"),
)
def set_playbackRate(value):
    return value


@app.callback(
    Output("player", "intervalCurrentTime"),
    Input("intervalCurrentTime-slider", "value"),
)
def set_intervalCurrentTime(value):
    return value


@app.callback(
    Output("player", "intervalSecondsLoaded"),
    Input("intervalSecondsLoaded-slider", "value"),
)
def set_intervalSecondsLoaded(value):
    return value


@app.callback(
    Output("player", "intervalDuration"),
    Input("intervalDuration-slider", "value"),
)
def set_intervalDuration(value):
    return value



# app = Dash(__name__)
#
# df = pd.read_csv('https://raw.githubusercontent.com/jebrus/DSC-180B-Final-Project/samhorio-patch-1/artist_data.csv_part0.csv?token=GHSAT0AAAAAACNQZT7AYCYVPTAPK6WNMXUEZOKZBUQ')
#
# fig = px.bar(df, x='artist_name', y='play_count', title='Top 10 Artists by Play Count')
#
# # App layout
# app.layout = html.Div([
#
#     html.Div(
#         [html.H1('Spotiversity', className='custom-header'),
#         html.H2('where you can discover your rhythm', className='subtitle-header')],
#         className='header-container'
#     ),
#     html.Div(children='first app w data :P'),
#     html.Div([
#         html.P('This is some example content below the header.')
#     ]),
#     dash_table.DataTable(data=df.to_dict('records'), page_size=10),
#     dcc.Graph(
#         id='artist-play-count-bar-chart',
#         figure=fig
#     )
# ])
#
if __name__ == '__main__':
    app.run_server(debug=True)
