import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests

import pandas as pd

ids = ['1','2','3','4','5','6','7','8','9','10','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','28','29','30']

years = ['20192020', '20182019', '20172018', '20162017', '20152016', '20142015', '20132014', '20122013', '20112012', '20102011']
years_slider = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011]

df = pd.DataFrame(columns =['gamesPlayed', 'wins', 'losses', 'ot', 'pts', 'ptPctg', 'goalsPerGame', 'goalsAgainstPerGame', 'evGGARatio', 'powerPlayPercentage', 'powerPlayGoals', 'powerPlayGoalsAgainst', 'powerPlayOpportunities', 'penaltyKillPercentage', 'shotsPerGame', 'shotsAllowed', 'winScoreFirst', 'winOppScoreFirst', 'winLeadFirstPer', 'winLeadSecondPer', 'winOutshootOpp', 'winOutshotByOpp', 'faceOffsTaken', 'faceOffsWon', 'faceOffsLost', 'faceOffWinPercentage', 'shootingPctg', 'savePctg', 'Team'] )
for year in years:
    teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams/4/?expand=team.stats&season='+year)

    team_name = teams.json()['teams'][0]['name']

    team_stats = teams.json()['teams'][0]['teamStats'][0]['splits'][0]['stat']

    team_stats['Year'] = year[-4:]

    df = df.append(team_stats, ignore_index = True)

df['Year'] = pd.to_numeric(df['Year'])

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(id='input-team',
            options=[
                {'label': 'New Jersey Devils', 'value': 1},
                {'label': 'New York Islanders', 'value': 2},
                {'label': 'New York Rangers', 'value': 3},
                {'label': 'Philadelphia Flyers', 'value': 4},
                {'label': 'Pittsburgh Penguins', 'value': 5},
                {'label': 'Boston Bruins', 'value': 6},
                {'label': 'Buffalo Sabres', 'value': 7},
                {'label': 'Montreal Canadiens', 'value': 8},
                {'label': 'Ottawa Senators', 'value': 9},
                {'label': 'Toronto Maple Leafs', 'value': 10},
                {'label': 'Carolina Hurricanes', 'value': 12},
                {'label': 'Florida Panthers', 'value': 13},
                {'label': 'Tampa Bay Lightning', 'value': 14},
                {'label': 'Washington Capitals', 'value': 15},
                {'label': 'Chicago Blackhawks', 'value': 16},
                {'label': 'Detroit Red Wings', 'value': 17},
                {'label': 'Nashville Predators', 'value': 18},
                {'label': 'St. Louis Blues', 'value': 19},
                {'label': 'Calgary Flames', 'value': 20},
                {'label': 'Colorado Avalanche', 'value': 21},
                {'label': 'Edmonton Oilers', 'value': 22},
                {'label': 'Vancouver Canucks', 'value': 23},
                {'label': 'Anaheim Ducks', 'value': 24},
                {'label': 'Dallas Stars', 'value': 25},
                {'label': 'Los Angeles Kings', 'value': 26},
                {'label': 'San Jose Sharks', 'value': 28},
                {'label': 'Columbus Blue Jackets', 'value': 29},
                {'label': 'Minnesota Wild', 'value': 30},
                {'label': 'Winnipeg Jets', 'value': 52},
                {'label': 'Arizona Coyotes', 'value': 53},
                {'label': 'Vegas Golden Knights', 'value': 54},
                {'label': 'Seattle Kraken', 'value': 55},
                ],
            placeholder='Select a Team',
            value = 4,
            style={'width':'80%','padding':'3px','font-size':'20px','text-align':'center'}),
    dcc.Dropdown(id='input-year',
            options=[
                {'label': '2011', 'value': 2011},
                {'label': '2012', 'value':2012}
                ],
            placeholder='Select a Year',
            value = 2011,
            style={'width':'80%','padding':'3px','font-size':'20px','text-align':'center'}),
    html.Div([
        dcc.Graph(id='graph-with-slider'),
    ]),
    html.Div([
        generate_table(df),
    ])
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('input-year', 'value'),
    Input('input-team', 'value'))
def update_figure(selected_year, team):
    filtered_df = df[(df['Year']>= (int(selected_year) - 2)) & (df['Year']<= (int(selected_year) + 2))]

    fig = px.line(filtered_df, x="Year", y =["goalsPerGame", 'goalsAgainstPerGame'] )

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
