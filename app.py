import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests

import pandas as pd

## TODO: make sure table updates, figure out why year options , update the for years in year part of the df building loop.  Change it so that for each team it grabs every year past the starting year that appears in the api summary for their team

ids = ['1','2','3','4','5','6','7','8','9','10','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','28','29','30', '52']
#figure out why 53 arizona coyotes, and 54, vegas golden knights break the script

years = ['20002001','20012002','20022003','20032004','20052006','20062007','20072008','20082009','20092010','20102011','20112012','20122013','20132014','20142015','20152016','20162017','20172018','20182019','20192020','20202021']

df = pd.DataFrame(columns =['gamesPlayed', 'wins', 'losses', 'ot', 'pts', 'ptPctg', 'goalsPerGame', 'goalsAgainstPerGame', 'evGGARatio', 'powerPlayPercentage', 'powerPlayGoals', 'powerPlayGoalsAgainst', 'powerPlayOpportunities', 'penaltyKillPercentage', 'shotsPerGame', 'shotsAllowed', 'winScoreFirst', 'winOppScoreFirst', 'winLeadFirstPer', 'winLeadSecondPer', 'winOutshootOpp', 'winOutshotByOpp', 'faceOffsTaken', 'faceOffsWon', 'faceOffsLost', 'faceOffWinPercentage', 'shootingPctg', 'savePctg', 'Team'] )
for i in ids:
    #First get what years teams played, that way we only pull data from years where data exists
    teamdata = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + i)
    year1 = teamdata.json()['teams'][0]['firstYearOfPlay']
    if id == '53':
        #A specific carve out is made for the Yotes, as there start year doesn't match the first year stats exist, as a result of the org being passed around a few times
        startpoint = years[-7]
    elif int(year1) < int(years[0][0:4]):
        startpoint = 0
    else:
        yearstring = year1 + str(int(year1) +1)
        startpoint = years.index(yearstring)

    for year in years[startpoint:]:
        teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + i +'/?expand=team.stats&season='+year)

        team_name = teams.json()['teams'][0]['name']

        team_stats = teams.json()['teams'][0]['teamStats'][0]['splits'][0]['stat']

        team_stats['Year'] = year[-4:]
        team_stats['Team'] = team_name

        df = df.append(team_stats, ignore_index = True)

df['Year'] = pd.to_numeric(df['Year'])

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
                {'label': 'New Jersey Devils', 'value': 'New Jersey Devils'},
                {'label': 'New York Islanders', 'value': 'New York Islanders'},
                {'label': 'New York Rangers', 'value': 'New York Rangers'},
                {'label': 'Philadelphia Flyers', 'value': 'Philadelphia Flyers'},
                {'label': 'Pittsburgh Penguins', 'value': 'Pittsburgh Penguins'},
                {'label': 'Boston Bruins', 'value': 'Boston Bruins'},
                {'label': 'Buffalo Sabres', 'value': 'Buffalo Sabres'},
                {'label': 'Montréal Canadiens', 'value': 'Montréal Canadiens'},
                {'label': 'Ottawa Senators', 'value': 'Ottawa Senators'},
                {'label': 'Toronto Maple Leafs', 'value': 'Toronto Maple Leafs'},
                {'label': 'Carolina Hurricanes', 'value': 'Carolina Hurricanes'},
                {'label': 'Florida Panthers', 'value': 'Florida Panthers'},
                {'label': 'Tampa Bay Lightning', 'value': 'Tampa Bay Lightning'},
                {'label': 'Washington Capitals', 'value': 'Washington Capitals'},
                {'label': 'Chicago Blackhawks', 'value': 'Chicago Blackhawks'},
                {'label': 'Detroit Red Wings', 'value': 'Detroit Red Wings'},
                {'label': 'Nashville Predators', 'value': 'Nashville Predators'},
                {'label': 'St. Louis Blues', 'value': 'St. Louis Blues'},
                {'label': 'Calgary Flames', 'value': 'Calgary Flames'},
                {'label': 'Colorado Avalanche', 'value': 'Colorado Avalanche'},
                {'label': 'Edmonton Oilers', 'value': 'Edmonton Oilers'},
                {'label': 'Vancouver Canucks', 'value': 'Vancouver Canucks'},
                {'label': 'Anaheim Ducks', 'value': 'Anaheim Ducks'},
                {'label': 'Dallas Stars', 'value': 'Dallas Stars'},
                {'label': 'Los Angeles Kings', 'value': 'Los Angeles Kings'},
                {'label': 'San Jose Sharks', 'value': 'San Jose Sharks'},
                {'label': 'Columbus Blue Jackets', 'value': 'Columbus Blue Jackets'},
                {'label': 'Minnesota Wild', 'value': 'Minnesota Wild'},
                {'label': 'Winnipeg Jets', 'value': 'Winnipeg Jets'},
                {'label': 'Arizona Coyotes', 'value': 'Arizona Coyotes'},
                {'label': 'Vegas Golden Knights', 'value': 'Vegas Golden Knights'},
                ],
            placeholder='Select a Team',
            value = 'Philadelphia Flyers',
            style={'width':'80%','padding':'3px','font-size':'20px','text-align':'center'}),
    dcc.Dropdown(id ='year-options'),
    html.Div([
        dcc.Graph(id='graph-with-slider'),
    ]),
    html.Div([
        generate_table(df),
    ])
])

@app.callback(
        Output('year-options', 'options'),
        Input('input-team', 'value'),
)
def set_year_options(team_name):
    filtered_df = df[df['Team'] == 'Philadelphia Flyers']
    years_dict = {}
    for year in filtered_df['Year']:
        years_dict[year] = year
    return[{'label':i, 'value':i} for i in years_dict]


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-options', 'value'),
    Input('input-team', 'value'),
    )
def update_figure(selected_year, team):
    filtered_df = df[df['Team'] == team]
    filtered_df = filtered_df[(filtered_df['Year']>= (int(selected_year) - 2)) & (df['Year']<= (int(selected_year) + 2))]

    fig = px.line(filtered_df, x="Year", y =["goalsPerGame", 'goalsAgainstPerGame'] )

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
