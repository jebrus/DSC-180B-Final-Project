import dash
from dash import Dash, dcc, html, dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
from dash import Dash, html, Input, Output, State
#import dash_player as dp
import dash_player
import re

app = Dash(__name__)

def query(artists: list, n: int) -> list:
    if artists:
        return artists * n  # Example output
    else:
        raise ValueError('No artists provided.')

app.layout = html.Div([
    # Header section
    html.Div(
        [html.H1('Discover Your Rhythm', className='custom-header'),
         html.H2('Where you can discover new artists both near and far!', className='subtitle-header')],
        className='header-container'
    ),

    # # original input section for artist recommendations/searches
    # dcc.Input(id='artist-input', type='text', placeholder='Enter artists you like separated by comma', className='artist-input'),
    # html.Button('Submit', id='submit-val', n_clicks=0, className='submit-button'),
    # html.Div(id='recommendation-output', className='recommendation-output'),

    # #3 input fields for artist recommendations/searches
    # html.Label(' Enter the name of the first artist:'),
    # dcc.Input(id='input-1-state', type='text', value='', className='artist-input'),
    # html.Label('   Second artist:'),
    # dcc.Input(id='input-2-state', type='text', value='', className='artist-input'),
    # html.Label('   Third artist:'),
    # dcc.Input(id='input-3-state', type='text', value='', className='artist-input'),
    # html.Button('Submit', id='submit-val', n_clicks=0, className='submit-button'),
    # html.Div(id='recommendation-output', className='recommendation-output'),

    dcc.Input(id='artist-input', type='text', placeholder='Enter artists you like separated by commas', debounce=True, className='artist-input', style={'width': '90%'}),
    html.Button('Submit', id='submit-val', n_clicks=0, className='submit-button'),
    html.Div(id='artist-list', className='artist-list'),

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


# for 20 artists
@app.callback(
    Output('artist-list', 'children'),
    Input('submit-val', 'n_clicks'),
    State('artist-input', 'value')
)
# new "update_output" for 20 artists
def update_artist_list(n_clicks, input_value):
    if n_clicks > 0 and input_value:
        try:
            # Parse the input value to get a list of artist names
            artist_names = parse_artist_input(input_value)
            # Convert the list to a bullet-pointed list to display on the page
            return html.Ul([html.Li(artist) for artist in artist_names])
        except Exception as e:
            return f"An error occurred: {e}"
    return "Enter artist names and press submit."

# Leave this portion untouched^^

# Need to check with team how much we care about the actual video playback stuff


# Artists with commas in their names
artist_comma_names = ['Does It Offend You, Yeah?', 'Tyler, the Creator', 'Chunk! No, Captain Chunk!', 'Drop Dead, Gorgeous', 'Kagrra,', 'Sammy Davis, Jr.', 'Now, Now Every Children', 'Now, Now', 'Meanwhile, Back in Communist Russia...', '2TM2,3', 'Medeski, Martin and Wood', 'Fear, and Loathing in Las Vegas', 'Albert Hammond, Jr.', 'Jump, Little Children', 'Ja, Panik', 'Леонид Фёдоров, Владимир Волков, Джон Медески, Марк Рибо', 'Right Away, Great Captain!', 'Fire! Santa Rosa, Fire!', 'Us, From Outside', 'Andrew Manze, Richard Egarr', '10,000 Maniacs', 'A Life, A Song, A Cigarette', 'Our Hollow, Our Home', 'Fibes, Oh Fibes!', 'I, Robot', 'Raz, Dwa, Trzy', 'Dream On, Dreamer', 'Harry Connick, Jr.', 'You, Me, and Everyone We Know', 'Hollywood, Mon Amour', "Volcano, I'm Still Excited!!", 'Chopin, Frédéric', 'Yes, Mama OK?', 'Invent, Animate', 'Queen Latifah, Nikki Blonsky, Zac Efron and Elijah Kelley', 'Duke Ellington, Charles Mingus, Max Roach', 'Oh, Sleeper', '¡Forward, Russia!', 'football, etc.', 'Emerson, Lake and Palmer', 'Apologies, I Have None', 'Sydän, sydän', 'Up, Bustle and Out', 'Russell Brower, Derek Duke, Matt Uelmen', 'Earth, Wind and Fire', 'Nitty Scott, MC', 'Nashville Symphony Orchestra, Kenneth Schermerhorn', 'A Fine Boat, That Coffin!', 'Wiener Philharmoniker, Claudio Abbado', 'Grover Washington, Jr.', 'Bach, Johann Sebastian', 'Son, Ambulance', 'Joshua Bell, Edgar Meyer, Sam Bush, Mike Marshall', 'Anouar Brahem, John Surman, Dave Holland', '10,000 Things', 'Fingers-Cut, Megamachine!', "Captain, We're Sinking", 'Kid Cudi, Best Coast and Rostam of Vampire Weekend', 'Beta Band, The', 'I, The Breather', 'Reinhold Heil, Johnny Klimek, Tom Tykwer', 'Barbara Bonney, Malcolm Martineau', 'The Choir Of Trinity College, Cambridge', 'Oh, Atoms', 'Roger Waters, Van Morrison, The Band', 'Fertig, Los!', 'Леонид Фёдоров, Владимир Волков', 'Daisuke Ishiwatari, Koh-ichi Seiyama', 'Alumiinium, sinu sädelev sõber', 'Nice Wings, Icarus!', 'Hello, Blue Roses', 'Jan Garbarek, Anouar Brahem, Shaukat Hussain', 'Last, James', 'Hui Buh, das Schlossgespenst', 'Barbara Melzer, Iwona Zasuwa, Anna Frankowska', 'Wolfgang Schneiderhan, Carl Seemann', "Choir of King's College, Cambridge", "King's College Choir, Cambridge", 'Suddenly, Tammy!', 'Кобыла И Трупоглазые Жабы Искали Цезию, Нашли Поздно Утром Свистящего Хна', 'Fuck Her, Or the Terrorists Win', 'Overhead, The Albatross', 'John Eliot Gardiner, The English Baroque Soloists, The Monteverdi Choir', 'Träd, Gräs och Stenar', 'Teleport me, Johny', 'Lonely, dear', "Mix Speaker's,Inc.", 'Pretentious, Moi?', 'Kirov Orchestra, Valery Gergiev', 'Анри Волохонский, Алексей Хвостенко, Леонид Фёдоров, Владимир Волков', 'Halloween, Alaska', 'Jun Ishikawa, Hirokazu Ando', 'Ice, Sea, Dead People', 'Zac Efron, Nikki Blonsky, Elijah Kelley and Amanda Bynes', 'Händel, Georg Friedrich', 'Martin Luther King, Jr.', 'hélas,whale', 'András Keller, János Pilz', 'She, Sir', 'Wow, Owls!', 'Earl Scruggs, Doc Watson and Ricky Skaggs', 'I, Parasite', 'Farewell, My Love', 'Or, the Whale', 'Tracy W. Bush, Derek Duke, Jason Hayes, Glenn Stafford', 'What Price, Wonderland?', 'White Stripes, The', 'Thee, Stranded Horse', 'Sol Gabetta, Sonatori De La Gioiosa Marca', 'Alvy, Nacho y Rubin', 'Dietrich Fischer-Dieskau, Gerald Moore', "She's Spanish, I'm American", 'Letni, Chamski Podryw', 'Die, Emperor! Die!', 'Thomas Quasthoff, Justus Zeyen', 'Ian Bostridge, Julius Drake', "Fuck Art, Let's Dance!", 'Lipps, Inc.', 'Wake Up, Girls!', 'Johann Sebastian Bach, Glenn Gould', 'Argerich, Kremer, Maisky', 'Elomar, Geraldo Azevedo, Vital Farias, Xangai', "The Choir of King's College, Cambridge", 'Point Juncture, WA', 'City of Prague Philharmonic Orchestra, James Fitzpatrick', 'Monks of the Dip Tse Chok Ling Monastery, Dharamsala', 'The Birds Are Spies, They Report to the Trees', 'Collegium Vocale Gent, Philippe Herreweghe', 'Robert Earl Keen, Jr.', 'Viktoria Mullova, Piotr Anderszewski', 'Apes, Pigs and Spacemen', 'The Sea, Like Lead', 'Jerry Leiber, Mike Stoller', 'Goodnight, Texas', 'Frank Sinatra, Jr.', 'Noize MC, Кислый, Макс, Пашок', 'Wilbert Roget, II', 'Astronauts, etc.', 'Beach Boys, The', 'Gould, Glenn', 'Balthrop, Alabama', "シェリル・ノーム starring May'n, ランカ・リー=中島愛", 'Michiru Yamane, Takashi Yoshida, Masahiko Kimura', 'Chorus of the Royal Opera House, Covent Garden', 'The Opposites feat. Dio, Willie Wartaal', 'Mischa Maisky, Martha Argerich', 'Ambros, Tauchen, Fälbl', '30,000 Monkies', 'Sasha, Benny y Erik', 'Maggi, Pierce And E.J.', 'Tex, Don and Charlie', 'One Tail, One Head', 'your gold, my pink', 'Not Drowning, Waving', "André Navarra, Annie d'Arco", 'Animals, The', 'Cánovas, Rodrigo, Adolfo y Guzmán', "You, You're Awesome", 'London Symphony Orchestra, Benjamin Britten', 'Manack, MANYO (Little Wing)', 'Anne Gastinel, Claire Désert', 'Amy Sedaris, Paul Dinello, Stephen Colbert', 'Barrozo, Perini, Takara, Bistolfi, Leonetti', 'Stiffs, Inc.', 'Wolf Harden, Takako Nishizaki', 'Itzhak Perlman, Boston Symphony Orchestra, John Williams', 'Hespèrion XXI, Jordi Savall', 'Roderick Williams, Iain Burnside', 'Sukhwinder Singh, Sunidhi Chauhan', 'Tyler, The Creator Feat. Pharrell Williams', 'Tyler, the Creator feat. Tallulah', 'Afel Bocoum, Damon Albarn, Toumani Diabaté, Ko Kan Ko Sata', 'Brahms, Johannes', 'Tacks, the Boy Disaster', 'КОБЫЛА И ТРУПОГЛАЗЫЕ ЖАБЫ ИСКАЛИ ЦЕЗИЮ, НАШЛИ ПОЗДНО УТРОМ СВИСТЯЩЕГО ХНА', 'Jakszyk, Fripp and Collins', 'Dino, Desi and Billy', 'Jean-Guihen Queyras, Alexandre Tharaud', 'Staatskapelle Dresden, Wolfgang Sawallisch', 'The Sixteen, Harry Christophers', 'Everything, Now!', 'Fritz Wunderlich, Hubert Giesen', 'Tyler, The Creator feat. Hodgy Beats', 'Scarlatti, Alessandro', 'Guess Who, The', 'I, Omega', 'San Francisco Symphony, Herbert Blomstedt', 'David Oistrakh, Lev Oborin', 'Williams, Robbie', 'Look, Stranger!', 'The Sea, The Sea', 'Julia Fischer, Russian National Orchestra, Yakov Kreizberg', 'Tomasz Filipczak, Piotr Rodowicz i przyjaciele', 'I, Ludicrous', 'Slovak Chamber Orchestra, Bohdan Warchal', 'I, The Skyline', 'Ammer, Einheit, Haage', 'Schubert, Franz', 'Gil Shaham, Göran Söllscher', 'Se, josta ei puhuta', "The Choir of St George's Chapel, Windsor Castle", 'Selecter, The', '1,2,3', 'Martha Argerich, Mikhail Pletnev', 'John Greaves, Peter Blegvad, Lisa Herman', 'Riptides, The', '125, rue Montmartre', 'Rurals, The', 'Hollies, The', 'Elba Ramalho, Geraldo Azevedo', 'Trent Reznor, Peter Murphy, Jeordie White, Atticus Ross', 'Certainly, Sir', 'Martha Argerich, Nelson Freire', 'Pablo Ziegler, Quique Sinesi w. Walter Castro', 'Ensemble Modern, Ingo Metzmacher', 'Maria Callas, Giuseppe di Stefano', 'Anne Sofie Von Otter, Bengt Forsberg', 'Gushi, Raffunk', 'Ensemble Matheus, Jean-christophe Spinosi', 'Io, Carlo', 'Zbogom, Ajda', '제시카, 티파니, 서현', 'Trevor Pinnock, The English Concert', 'Edgar Meyer, Béla Fleck, Mike Marshall', 'Janine Jansen, Itamar Golan', 'Peja, Glon, Gandzior, Kaczor', 'Hespèrion XX, Jordi Savall', 'John T. Williams, Krzysztof Penderecki, Toshiro Mayzumi; Eastman Wind Ensemble, Donald Hunsberger', "Krzysztof Penderecki; Warsaw Philharmonic Orchestra, Warsaw Philharmonic Choir, Warsaw Boys' Choir, Antoni Wit", 'Steven Isserlis, Pascal Devoyon', 'Moore, Gary', 'Vivaldi, Corelli, Albinoni', 'Scott Henderson, Steve Smith, Victor Wooten', 'Flaming Lips, The', 'Ernst, Bobbie en de Rest', 'Ivete Sangalo, Gilberto Gil, Caetano Veloso', 'Paris, Texas', 'Le Concert Des Nations, Jordi Savall', 'Marilyn Crispell, Gary Peacock, Paul Motian', 'Eesti Keeled Ja Jaak Johanson, Riho Sibul', 'Mstislav Rostropovich, Rudolf Serkin', 'Isabelle Faust, Alexander Melnikov', 'Goons, The', 'Russell Brower, Derek Duke, Glenn Stafford', 'Alex, Jorge Y Lena', 'Orchestra of the Royal Opera House, Covent Garden', 'Eraldo Bernocchi, Harold Budd, Robin Guthrie', 'Sledě, živé sledě', "Rockin' Dopsie, Jr.", 'Paul Kandel, David Ogden Stiers, Tony Jay, Chorus', 'Itzhak Perlman, New York Philharmonic, Zubin Mehta', 'London Symphony Orchestra, Aaron Copland', 'Valery Gergiev, Kirov Orchestra', 'Lynn Harrell, James Levine', 'Masahiko Kimura, Norikazu Miura, Michiru Yamane', 'Anna Netrebko, Mahler Chamber Orchestra, Claudio Abbado', 'Cigarettes, the', 'Mirosław Czyżykiewicz, Hadrian Tabęcki, Jacek Bończyk', 'Bach Collegium Japan, Masaaki Suzuki', 'Фёдоров, Волков, Курашов', 'Herbert von Karajan, Berliner Philharmoniker', 'I Musici, Pina Carmirelli', 'Martha Argerich, Alexandre Rabinovitch', 'Jean-Pierre Rampal, Lily Laskine', 'Maurizio Pollini, Wiener Philharmoniker, Eugen Jochum', 'Albert Collins, Robert Cray and Johnny Copeland', 'Damin Eih, A.L.K. And Brother Clark', 'Wiener Philharmoniker, Georges Prêtre', 'Excision, Downlink and Space Laces', 'Slow Down, Molasses', 'Yuko Takehara, Masato Kouda', 'Mark Kosower, Jee-Won Oh', 'Håll Käften, Vad Vill Du!?', 'Bear Bones, Lay Low', 'Gil Shaham, Jonathan Feldman', 'Kishore Kumar, Lata Mangeshkar', 'Joshua Bell, Paul Coker', 'Anna Netrebko, Orchestra of the Mariinsky Theatre, Valery Gergiev', 'Musica Antiqua Köln, Reinhard Goebel', 'Taha, Khaled, Faudel', 'Borixon, Kajman', 'Arthur Grumiaux, Walter Klien', 'Fuck, The Retarded Girl', 'Oh, Manhattan', 'New York Philharmonic, Bruno Walter', 'Benedictines Of Mary, Queen Of Apostles', 'Paul McCartney, Linda McCartney', 'Peter, Sue und Marc', 'Sledě, Živé Sledě', 'Saffire, The Uppity Blues Women', 'Philharmonia Baroque Orchestra, Nicholas McGegan', 'Xerxes, Romeo Knight and Bendik', 'Michala Petri, Keith Jarrett', 'Magnus, Brasse Och Eva', 'Wyatt, Atzmon, Stephen', 'Employer, Employee', 'Common Eider, King Eider', 'Concertgebouw Orchestra, Bernard Haitink', 'A Rose, By Any Other Name', 'Michal, Patxi, Lukas Delcourt, Premix', 'Orchestre Révolutionnaire et Romantique, John Eliot Gardiner', 'Julian Bream, John Williams', 'Toshinori Kondo, Eraldo Bernocchi, Bill Laswell', 'Philadelphia Orchestra, Eugene Ormandy', 'Los Angeles, The Voices', 'London Philharmonic Orchestra, Klaus Tennstedt', 'donGURALesko feat. Sitek, Shellerini']

# Parsing artists without interfering with commas
def parse_artist_input(input_string):

    # Lowercase the input string for case-insensitive comparison
    input_string_lower = input_string.lower()
    artist_map = {artist.lower(): artist for artist in artist_comma_names}
    for artist_lower in artist_map:
        if artist_lower in input_string_lower:
            input_string_lower = input_string_lower.replace(artist_lower, artist_lower.replace(',', '|'))
    artist_list_lower = input_string_lower.split(',')
    artist_list = [artist_map.get(artist.replace('|', ',').strip(), artist.replace('|', ',').strip()) for artist in artist_list_lower]
    artist_list = artist_list[:20]
    return artist_list

# BELOW IS ALL VIDEO STUFF

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

if __name__ == '__main__':
    app.run_server(debug=True)


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
