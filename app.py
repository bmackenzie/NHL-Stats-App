import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd

## TODO: make sure table updates, figure out why year options , update the for years in year part of the df building loop.  Change it so that for each team it grabs every year past the starting year that appears in the api summary for their team
color_dict = {'New Jersey Devils':['black', 'red'], 'New York Islanders':['blue','orange'], 'New York Rangers':['blue','red'], 'Philadelphia Flyers':['orange', 'black'], 'Pittsburgh Penguins':['black','yellow'], 'Boston Bruins':['black','yellow'], 'Buffalo Sabres':['blue','yellow'], 'Montreal Canadiens':['red','blue'], 'Ottawa Senators': ['red','black'], 'Toronto Maple Leafs':['blue','silver'], 'Carolina Hurricanes': ['black','red'], 'Florida Panthers':['blue','red'], 'Tampa Bay Lightning':['silver','blue'], 'Washington Capitals': ['blue','red'], 'Chicago Blackhawks':['red','black'], 'Detroit Red Wings':['red','silver'], 'Nashville Predators':['yellow','blue'], 'St. Louis Blues':['blue','yellow'], 'Calgary Flames':['red','orange'], 'Colorado Avalanche':['red','blue'], 'Edmonton Oilers':['orange','blue'], 'Vancouver Canucks':['blue','silver'], 'Anaheim Ducks':['green','black'], 'Dallas Stars':['green','silver'], 'Los Angeles Kings':['black','silver'], 'San Jose Sharks':['green','black'], 'Columbus Blue Jackets':['red','blue'], 'Minnesota Wild':['green','red'], 'Winnipeg Jets':['blue','silver'], 'Arizona Coyotes':['green','red'], 'Vegas Golden Knights':['yellow','red']}

df = pd.read_csv('C:\\Users\\Brian\\dash\\NHL-Stats-App\\NHL-stats.csv', header=0)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

app.layout = html.Div([
    html.H1('Hockey Trends',
             style={'textAlign': 'center', 'color': 'white','font-size': 40, 'margin-bottom':'2em'}),
    html.H3('Select a Team',
             style={'textAlign': 'center', 'color': 'white','font-size': 30}),
    dcc.Dropdown(id='input-team',
            options=[
                {'label': 'New Jersey Devils', 'value': 'New Jersey Devils'},
                {'label': 'New York Islanders', 'value': 'New York Islanders'},
                {'label': 'New York Rangers', 'value': 'New York Rangers'},
                {'label': 'Philadelphia Flyers', 'value': 'Philadelphia Flyers'},
                {'label': 'Pittsburgh Penguins', 'value': 'Pittsburgh Penguins'},
                {'label': 'Boston Bruins', 'value': 'Boston Bruins'},
                {'label': 'Buffalo Sabres', 'value': 'Buffalo Sabres'},
                {'label': 'Montréal Canadiens', 'value': 'Montreal Canadiens'},
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
            style={'width':'80%','padding':'3px','font-size':'20px','text-align':'center', 'margin':'auto'}),
    html.H3('Select a Year',
             style={'textAlign': 'center', 'color': 'white','font-size': 30}),
    dcc.Dropdown(id ='year-options', style={'width':'80%','padding':'3px','font-size':'20px','text-align':'center', 'margin':'auto'}, value ="2020"),
    html.H3('Select Visualizations',
             style={'textAlign': 'center', 'color': 'white','font-size': 30}),
    dcc.Checklist(id='input-graphs',
    options=[
        {'label': 'Point Percentage', 'value': 'points'},
        {'label': 'Goals Per Game', 'value': 'goals'},
        {'label': 'Goals Against Per Game', 'value': 'goals against'},
        {'label': 'Even Strength Goals/Goals Against Ratio', 'value': 'evgga'},
        {'label': 'Power Play Percentage', 'value': 'pp'},
        {'label': 'Penalty Kill Percentage', 'value': 'pk'},
        {'label': 'Faceoffs Win Percentage', 'value': 'faceoffs'},
        {'label': 'Save Percentage', 'value': 'saves'}
    ],
    value=['points', 'goals', 'goals against', 'evgga', 'pp', 'pk', 'faceoffs', 'saves'],
    labelStyle={'display': 'inline-block'},
    style={'width':'80%','padding':'3px','font-size':'20px','text-align':'center', 'margin':'auto', 'color':'white'}
    ),

    dbc.Row(
        [
            dbc.Col(html.Div([], id='plot1'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
            dbc.Col(html.Div([], id='plot2'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
        ]
    ),

    dbc.Row(
        [
            dbc.Col(html.Div([], id='plot3'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
            dbc.Col(html.Div([], id='plot4'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
        ]
    ),

    dbc.Row(
        [
            dbc.Col(html.Div([], id='plot5'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
            dbc.Col(html.Div([], id='plot6'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
        ]
    ),

    dbc.Row(
        [
            dbc.Col(html.Div([], id='plot7'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
            dbc.Col(html.Div([], id='plot8'),
            lg={'size':6, 'offset':0}, md={'size':8, 'offset':2}),
        ]
    ),
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
    Output(component_id='plot1', component_property='children'),
    Output(component_id='plot2', component_property='children'),
    Output(component_id='plot3', component_property='children'),
    Output(component_id='plot4', component_property='children'),
    Output(component_id='plot5', component_property='children'),
    Output(component_id='plot6', component_property='children'),
    Output(component_id='plot7', component_property='children'),
    Output(component_id='plot8', component_property='children'),
    Input('year-options', 'value'),
    Input('input-team', 'value'),
    Input('input-graphs', 'value'),
    )
def update_figure(selected_year, team, graphs):
    #make graphs based on checkboxes
    filtered_df = df[df['Team'] == team]
    filtered_df = filtered_df[(filtered_df['Year']>= (int(selected_year) - 5)) & (filtered_df['Year']<= (int(selected_year) + 5))]

    avg_df = df[df['Team'] == 'League Median']
    filtered_avg_df = avg_df[(avg_df['Year']>= (int(selected_year) - 5)) & (avg_df['Year']<= (int(selected_year) + 5))]

    team=filtered_df['Team'].unique()[0]
    colors = color_dict[team]

    pointsFig = px.line(filtered_df, x="Year", y =["ptPctg"], title ='Point Percentage by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'Point Percentage', 'variable':'legend'})
    pointsFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['ptPctg'], mode='lines', name='League Median', line=dict(color=colors[1])))
    pointsFig.for_each_trace(lambda t: t.update(name = {'ptPctg':team, 'League Median': 'League Median'}[t.name]))
    goalsFig = px.line(filtered_df, x = "Year", y = ['goalsPerGame'], title = 'Goals Per Game by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'Goals Per Game', 'variable':'legend'})
    goalsFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['goalsPerGame'], mode='lines', name='League Median', line=dict(color=colors[1])))
    goalsFig.for_each_trace(lambda t: t.update(name = {'goalsPerGame':team, 'League Median': 'League Median'}[t.name]))
    gaFig = px.line(filtered_df, x = "Year", y = ['goalsAgainstPerGame'], title = 'Goals Against Per Game by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'Goals Against Per Game', 'variable':'legend'})
    gaFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['goalsAgainstPerGame'], mode='lines', name='League Median', line=dict(color=colors[1])))
    gaFig.for_each_trace(lambda t: t.update(name = {'goalsAgainstPerGame':team, 'League Median': 'League Median'}[t.name]))
    evggaFig = px.line(filtered_df, x = "Year", y = ['evGGARatio'], title = 'Even Strength Goals/Goals Agaisnt Ratio by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'evGGA Ratio', 'variable':'legend'})
    evggaFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['evGGARatio'], mode='lines', name='League Median', line=dict(color=colors[1])))
    evggaFig.for_each_trace(lambda t: t.update(name = {'evGGARatio':team, 'League Median': 'League Median'}[t.name]))
    ppFig = px.line(filtered_df, x = "Year", y = ['powerPlayPercentage'], title = 'Power Play Percentage by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'Power Play Percentage', 'variable':'legend'})
    ppFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['powerPlayPercentage'], mode='lines', name='League Median', line=dict(color=colors[1])))
    ppFig.for_each_trace(lambda t: t.update(name = {'powerPlayPercentage':team, 'League Median': 'League Median'}[t.name]))
    pkFig = px.line(filtered_df, x = "Year", y = ['penaltyKillPercentage'], title = 'Penalty Kill Percentage by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'Penalty Kill Percentage', 'variable':'legend'})
    pkFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['penaltyKillPercentage'], mode='lines', name='League Median', line=dict(color=colors[1])))
    pkFig.for_each_trace(lambda t: t.update(name = {'penaltyKillPercentage':team, 'League Median': 'League Median'}[t.name]))
    faceoffsFig = px.line(filtered_df, x = "Year", y = ['faceOffWinPercentage'], title = 'Faceoff Win Percentage by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'Faceoff Win Percentage', 'variable':'legend'})
    faceoffsFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['faceOffWinPercentage'], mode='lines', name='League Median', line=dict(color=colors[1])))
    faceoffsFig.for_each_trace(lambda t: t.update(name = {'faceOffWinPercentage':team, 'League Median': 'League Median'}[t.name]))
    saveFig = px.line(filtered_df, x = "Year", y = ['savePctg'], title = 'Save Percentage by Year', color_discrete_sequence = [colors[0]], template="plotly", labels={'Year':'Year', 'value':'Save Percentage', 'variable':'legend'})
    saveFig.add_trace(go.Scatter(x=filtered_avg_df['Year'], y=filtered_avg_df['savePctg'], mode='lines', name='League Median', line=dict(color=colors[1])))
    saveFig.for_each_trace(lambda t: t.update(name = {'savePctg':team, 'League Median': 'League Median'}[t.name]))

    graphsList = []
    titleList = []
    for graph in graphs:
        if graph == 'points':
            graphsList.append(pointsFig)
            titleList.append('Point Percentage by Year')
        elif graph == 'goals':
            graphsList.append(goalsFig)
            titleList.append('Goals Per Game By Year')
        elif graph == 'goals against':
            graphsList.append(gaFig)
            titleList.append('Goals Against Per Game by Year')
        elif graph == 'evgga':
            graphsList.append(evggaFig)
            titleList.append('Even Strength Goals/Goals Agaisnt Ratio by Yea')
        elif graph == 'pp':
            graphsList.append(ppFig)
            titleList.append('Power Play Percentage by Year')
        elif graph == 'pk':
            graphsList.append(pkFig)
            titleList.append('Penalty Kill Percentage by Year')
        elif graph == 'faceoffs':
            graphsList.append(faceoffsFig)
            titleList.append('Faceoff Percentage by Year')
        else:
            graphsList.append(saveFig)
            titleList.append('Save Percentage by Year')

    if len(graphsList) == 0:
        return(dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 1:
        return (dcc.Graph(figure=graphsList[0]), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 2:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 3:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 4:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Graph(figure=graphsList[3]), dcc.Markdown(), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 5:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Graph(figure=graphsList[3]), dcc.Graph(figure=graphsList[4]), dcc.Markdown(), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 6:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Graph(figure=graphsList[3]), dcc.Graph(figure=graphsList[4]), dcc.Graph(figure=graphsList[5]), dcc.Markdown(), dcc.Markdown())
    elif len(graphsList) == 7:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Graph(figure=graphsList[3]), dcc.Graph(figure=graphsList[4]), dcc.Graph(figure=graphsList[5]), dcc.Graph(figure=graphsList[6]), dcc.Markdown())
    elif len(graphsList) == 8:
        return (dcc.Graph(figure=graphsList[0]), dcc.Graph(figure=graphsList[1]), dcc.Graph(figure=graphsList[2]), dcc.Graph(figure=graphsList[3]), dcc.Graph(figure=graphsList[4]), dcc.Graph(figure=graphsList[5]), dcc.Graph(figure=graphsList[6]), dcc.Graph(figure=graphsList[7]))



if __name__ == '__main__':
    app.run_server(debug=True)
