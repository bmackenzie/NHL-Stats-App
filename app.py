import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests

import pandas as pd

## TODO: make sure table updates, figure out why year options , update the for years in year part of the df building loop.  Change it so that for each team it grabs every year past the starting year that appears in the api summary for their team
color_dict = {'New Jersey Devils':['black', 'red'], 'New York Islanders':['blue','orange'], 'New York Rangers':['blue','red'], 'Philadelphia Flyers':['orange', 'black'], 'Pittsburgh Penguins':['black','yellow'], 'Boston Bruins':['black','yellow'], 'Buffalo Sabres':['blue','yellow'], 'Montréal Canadiens':['red','blue'], 'Ottawa Senators': ['red','black'], 'Toronto Maple Leafs':['blue','white'], 'Carolina Hurricanes': ['black','red'], 'Florida Panthers':['blue','red'], 'Tampa Bay Lightning':['silver','blue'], 'Washington Capitals': ['blue','red'], 'Chicago Blackhawks':['red','black'], 'Detroit Red Wings':['red','white'], 'Nashville Predators':['yellow','blue'], 'St. Louis Blues':['blue','yellow'], 'Calgary Flames':['red','orange'], 'Colorado Avalanche':['red','blue'], 'Edmonton Oilers':['orange','blue'], 'Vancouver Canucks':['blue','white'], 'Anaheim Ducks':['green','black'], 'Dallas Stars':['green','white'], 'Los Angeles Kings':['black','white'], 'San Jose Sharks':['green','black'], 'Columbus Blue Jackets':['red','blue'], 'Minnesota Wild':['green','red'], 'Winnipeg Jets':['blue','white'], 'Arizona Coyotes':['green','red'], 'Vegas Golden Knights':['yellow','red']}

ids = ['1','2','3','4','5','6','7','8','9','10','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','28','29','30', '52', '53','54']

years = ['20002001','20012002','20022003','20032004','20052006','20062007','20072008','20082009','20092010','20102011','20112012','20122013','20132014','20142015','20152016','20162017','20172018','20182019','20192020','20202021']

df = pd.DataFrame(columns =['gamesPlayed', 'wins', 'losses', 'ot', 'pts', 'ptPctg', 'goalsPerGame', 'goalsAgainstPerGame', 'evGGARatio', 'powerPlayPercentage', 'powerPlayGoals', 'powerPlayGoalsAgainst', 'powerPlayOpportunities', 'penaltyKillPercentage', 'shotsPerGame', 'shotsAllowed', 'winScoreFirst', 'winOppScoreFirst', 'winLeadFirstPer', 'winLeadSecondPer', 'winOutshootOpp', 'winOutshotByOpp', 'faceOffsTaken', 'faceOffsWon', 'faceOffsLost', 'faceOffWinPercentage', 'shootingPctg', 'savePctg', 'Team'] )
for i in ids:
    print(i)
    teamdata = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + i)
    year1 = str(int(teamdata.json()['teams'][0]['firstYearOfPlay'])+1)
    if i == '53':
        startpoint = years.index(years[-7])
    elif int(year1) < int(years[0][0:4]):
        startpoint = 0
    else:
        yearstring = year1 + str(int(year1) +1)
        startpoint = years.index(yearstring)
    print(startpoint)

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
    dcc.Dropdown(id ='year-options', style={'width':'80%','padding':'3px','font-size':'20px','text-align':'center'}, value ="2020"),
    dcc.Checklist(id='input-graphs',
    options=[
        {'label': 'Wins and Losses', 'value': 'wins'},
        {'label': 'Goals and Goals Against', 'value': 'goals'},
        {'label': 'Special Teams', 'value': 'special-teams'},
        {'label': 'Shots Per Game and Shots Allowed', 'value': 'shots'},
        {'label': 'Faceoffs Won/Lost', 'value': 'faceoffs'}
    ],
    value=['wins', 'goals', 'special-teams', 'shots', 'faceoffs'],
    labelStyle={'display': 'inline-block'}
    ),
    html.Div([
        html.Div([], id='plot1'),
        html.Div([], id='plot2')
    ], style={'display': 'flex'}),

    html.Div([
            html.Div([], id='plot3'),
            html.Div([], id='plot4')
        ], style={'display': 'flex'}),

    html.Div([
            html.Div([], id='plot5'),
            html.Div([], id='plot6')
        ], style={'display': 'flex'}),
])

@app.callback(
        Output('year-options', 'options'),
        Input('input-team', 'value'),
)
def set_year_options(team_name):
    filtered_df = df[df['Team'] == team_name]
    years_dict = {}
    for year in filtered_df['Year']:
        years_dict[year] = year
    return[{'label':i, 'value':i} for i in years_dict]


@app.callback(
    #Output('graph-with-slider', 'figure'),
    Output(component_id='plot1', component_property='children'),
    Output(component_id='plot2', component_property='children'),
    Output(component_id='plot3', component_property='children'),
    Output(component_id='plot4', component_property='children'),
    Output(component_id='plot5', component_property='children'),
    Input('year-options', 'value'),
    Input('input-team', 'value'),
    Input('input-graphs', 'value'),
    )
def update_figure(selected_year, team, graphs):
    #make graphs based on checkboxes
    if 'wins' in graphs:
        print('test')

    filtered_df = df[df['Team'] == team]
    filtered_df = filtered_df[(filtered_df['Year']>= (int(selected_year) - 2)) & (df['Year']<= (int(selected_year) + 2))]

    team=filtered_df['Team'].unique()[0]
    colors = color_dict[team]

    goalsFig = px.line(filtered_df, x="Year", y =["goalsPerGame", 'goalsAgainstPerGame'], title ='Goals vs Goals Against Per Game', color_discrete_map = {'goalsPerGame':colors[0], 'goalsAgainstPerGame':colors[1]})
    winsFig = px.line(filtered_df, x = "Year", y = ['wins', 'losses'], title = 'Wins vs Losses', color_discrete_map = {'wins':colors[0], 'losses':colors[1]})
    specialFig = px.line(filtered_df, x = 'Year', y=['powerPlayPercentage', 'penaltyKillPercentage'], title = 'Power Play Percentage vs Penalty Kill Percentage', color_discrete_map = {'powerPlayPercentage':colors[0], 'penaltyKillPercentage':colors[1]})
    shotsFig = px.line(filtered_df, x='Year', y=['shotsPerGame', 'shotsAllowed'], title = 'Shots vs Shots Allowed Per Game', color_discrete_map = {'shotsPerGame':colors[0], 'shotsAllowed':colors[1]})
    faceoffsFig = px.line(filtered_df, x='Year', y=['faceOffsWon', 'faceOffsLost'], title = 'Faceoffs Wins vs Losses', color_discrete_map = {'faceOffsWon':colors[0], 'faceOffsLost':colors[1]})
    #fig.update_layout(transition_duration=500)

    graphsList = []
    titleList = []
    for graph in graphs:
        if graph == 'wins':
            graphsList.append(winsFig)
            titleList.append('Wins vs Losses')
        elif graph == 'goals':
            graphsList.append(goalsFig)
            titleList.append('Goals vs Goals Against')
        elif graph == 'special-teams':
            graphsList.append(specialFig)
            titleList.append('Power Play Percentage vs Penalty Kill Percantage')
        elif graph == 'shots':
            graphsList.append(shotsFig)
            titleList.append('Shots vs Shots Allowed')
        else:
            graphsList.append(faceoffsFig)
            titleList.append('Faceoff Wins vs Losses')

    if len(graphsList) == 0:
        return(dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 1:
        return (dcc.Graph(figure=graphsList[0]), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 2:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 3:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 4:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Graph(figure=graphsList[3]), dcc.Markdown())
    elif len(graphsList) == 5:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Graph(figure=graphsList[3]), dcc.Graph(figure=graphsList[4]))



if __name__ == '__main__':
    app.run_server(debug=True)
