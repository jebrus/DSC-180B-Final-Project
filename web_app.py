# -*- coding: utf-8 -*-
import dash
from dash import Dash, dcc, html, dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State, ALL
from dash import Dash, html, Input, Output, State, dash_table
import dash_player
import re
from predictor import Predictor

app = Dash(__name__, assets_folder='web_app_assets', suppress_callback_exceptions=True)

model = Predictor()
underrepresented_weight, popularity_weight = 25, 200

def query(artists: list, n: int) -> list:
    if artists:
        return model.recommend(artists, n, underrepresented_weight, popularity_weight)
    else:
        raise ValueError('No artists provided.')

reviews = []

app.layout = html.Div([
    # Header section
    html.Div(
        className='header-container',
        children=[
            html.Div(
                className='header-title-container',
                children=[
                    html.Img(src=app.get_asset_url('web_app_logo.png'), className='custom-header')
                ]
            ),
            html.Div(
                className='search-bar-container',
                children=[
                    html.Div('Find new artists, both near and far!', className='search-bar-text'),
                    dcc.Input(
                        id='artist-input',
                        type='text',
                        placeholder='Enter artists you like separated by commas',
                        debounce=True,
                        className='artist-input'
                    ),
                    html.Button('Submit', id='submit-val', n_clicks=0, className='submit-button')
                ]
            )
        ]
    ),html.Div(id='artist-list'),\
    html.Nav(
        className='nav-menu',
        children=[
            html.Ul(
                children=[
                    html.Li(dcc.Link('HOME', href='/')),
                    html.Li(dcc.Link('ABOUT', href='/about')),
                    html.Li(dcc.Link('YOUR RECOMMENDATIONS', href='/recommendations')),
                    html.Li(dcc.Link('CONTACT', href='/contact')), \
                    html.Li(dcc.Link('REVIEWS', href='/reviews')),
                ]
            ),
        ]
    ), \
    html.Div(id='page-content', className='page-content'), \
    dcc.Location(id='url', refresh=False), \
    dcc.Store(id='stored-recommendations', storage_type='session'), \
    html.Img(
    src=app.get_asset_url('vinyl.png'),
    className='bottom-right-image'
)])


# For the menu/pages
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname'), Input('stored-recommendations', 'data')])
def display_page(pathname, stored_data):
    if pathname == '/about':
        return html.Div([
            html.Div(className='white-background', children=[
                html.H1("About Our Web App"),
            ]),
            html.Div(className='green-background', children=[
                html.P("Our music recommender offers a unique set of features designed for personalized music discovery. . Users can input their favorite artists to receive a curated list of recommended artists tailored to their individual tastes, focusing primarily on promoting musical diversity. Unlike conventional music recommenders, our system prioritizes suggestions from musically underrepresented countries, stepping away from the mainstream markets of the US, UK, and Canada. This approach not only broadens the spectrum of musical landscapes and cultures available to users but also highlights more obscure and emerging artists. By doing so, we provide an avenue for the exploration of unique sounds and styles not typically found in commercial charts, encouraging users to discover new music that they might not encounter elsewhere.")  # rest of your paragraph
            ])
        ])
    elif pathname == '/recommendations':
        if stored_data:
            recommendations_list = html.Ul([html.Li(artist) for artist in stored_data])
        else:
            recommendations_list = "No recommendations yet. Please submit some artists to get started."
        return html.Div([
            html.Div(className='white-background', children=[
                html.H1("Your Saved Recommendations"),
            ]),
            recommendations_list,
            html.Button('Refresh', id='refresh-button', n_clicks=0, className='refresh-button', style={'display': 'none'})
        ])
    elif pathname == '/contact':
        return html.Div([
            # Content for the Contact page
            html.Div(className='white-background', children=[
                html.H1("Having Issues?"),
            ]),
            html.P("Contact: Sam Horio (949) 491 - 3220. Collaborators: Joshua Brusewitz, Shivani Suther, Natalie Wu")
        ])
    elif pathname == '/reviews':
        return html.Div([
            html.Div(className='white-background', children=[
                html.H1("Thoughts? Anything you'd like to see? Let us know!"),
            ]),
            dcc.Textarea(
                id='review-text',
                placeholder='Enter your review here...',
                style={'width': '95%', 'height': 100, 'margin': '0 auto'},
            ),
            html.Button('Post Review', id='post-review-button', n_clicks=0),
            html.Div(id='reviews-container', children=generate_reviews_html())
        ])
    else:
        # Default to home page
        return html.Div([
            # Home page content
            html.Div(className='white-background', children=[
                html.H1("Welcome!"),
            ]),
            html.P("To get started, please click on 'Your Recommendations', then in the search bar input all your favorite artists, and receive a curated list of artists we think you'll like. To locate your recommendations, please click 'Your Recommendations'")
        ])

@app.callback(
    Output('reviews-container', 'children'),
    [Input('post-review-button', 'n_clicks')],
    [State('review-text', 'value')]
)

def post_review(n_clicks, review_text):
    if n_clicks > 0 and review_text:
        review_id = len(reviews)  # Unique ID for each review
        reviews.append({'id': review_id, 'text': review_text})
        return generate_reviews_html()
    return dash.no_update

# Callback for deleting a review
@app.callback(
    Output({'type': 'review', 'index': ALL}, 'style'),
    [Input({'type': 'delete-review-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'review', 'index': ALL}, 'id')]
)
def delete_review(n_clicks_list, ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [{}] * len(ids)
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    delete_review_id = json.loads(button_id)['index']

    global reviews
    reviews = [review for review in reviews if review['id'] != delete_review_id]

    return [{'display': 'none'} if id['index'] == delete_review_id else {} for id in ids]

# Function to generate reviews HTML
def generate_reviews_html():
    return [html.Div([
        html.P(review['text']),
        html.Button('Delete', id={'type': 'delete-review-button', 'index': review['id']}, n_clicks=0)
    ], id={'type': 'review', 'index': review['id']}, style={'border': '1px solid black', 'padding': '10px', 'margin': '10px 0'}) for review in reviews]


@app.callback(
    Output('refresh-button', 'style'),
    [Input('url', 'pathname')]
)

def toggle_refresh_button_visibility(pathname):
    if pathname == '/recommendations':
        return {'display': 'block'}  # Show the button
    return {'display': 'none'}  # Hide the button


@app.callback(
    [Output('artist-list', 'children'), Output('stored-recommendations', 'data')],
    [Input('submit-val', 'n_clicks'), Input('refresh-button', 'n_clicks')],
    [State('artist-input', 'value'), State('stored-recommendations', 'data')]
)
def update_and_clear_recommendations(submit_n_clicks, refresh_n_clicks, input_value, stored_data):
    ctx = dash.callback_context

    if not ctx.triggered:
        # No button has been clicked yet
        return "Enter artist names and press submit.", stored_data

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "submit-val" and input_value:
        try:
            artist_names = parse_artist_input(input_value)
            recommended_artists = query(artist_names, 10)  # Assuming 10 is the desired number of recommendations
            new_stored_data = list(set(stored_data + recommended_artists)) if stored_data else recommended_artists
            formatted_artist_list = 'Based on your most recent searches we recommend: ' + ', '.join(recommended_artists)
            return html.Div(formatted_artist_list), new_stored_data
        except Exception as e:
            return f"An error occurred: {e}", stored_data
    elif button_id == "refresh-button":
        # Clear the recommendations when refresh button is clicked
        return "Enter artist names and press submit.", []

    # Return nothing if there's no input or no clicks
    return dash.no_update, stored_data


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

if __name__ == '__main__':
    app.run_server(debug=True)
