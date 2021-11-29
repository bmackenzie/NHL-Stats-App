#List of ids that the API associates with each team
ids = ['1','2','3','4','5','6','7','8','9','10','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','28','29','30', '52', '53','54']

#List of years we are collecting data on
years = ['20002001','20012002','20022003','20032004','20052006','20062007','20072008','20082009','20092010','20102011','20112012','20122013','20132014','20142015','20152016','20162017','20172018','20182019','20192020','20202021']

df = pd.DataFrame(columns =['gamesPlayed', 'wins', 'losses', 'ot', 'pts', 'ptPctg', 'goalsPerGame', 'goalsAgainstPerGame', 'evGGARatio', 'powerPlayPercentage', 'powerPlayGoals', 'powerPlayGoalsAgainst', 'powerPlayOpportunities', 'penaltyKillPercentage', 'shotsPerGame', 'shotsAllowed', 'winScoreFirst', 'winOppScoreFirst', 'winLeadFirstPer', 'winLeadSecondPer', 'winOutshootOpp', 'winOutshotByOpp', 'faceOffsTaken', 'faceOffsWon', 'faceOffsLost', 'faceOffWinPercentage', 'shootingPctg', 'savePctg', 'Team'] )
#Loop through ids to get stats for each team, for each year, append that as a row to the data frame
for i in ids:
    teamdata = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + i)
    #determine first year of play and only collect data from that year forward
    year1 = str(int(teamdata.json()['teams'][0]['firstYearOfPlay'])+1)
    #Arizona Coyotes get a special carve out because the API has their first year listed as before the organization moved, but keeps those stats under a different ID
    if i == '53':
        startpoint = years.index(years[-7])
    elif int(year1) < int(years[0][0:4]):
        startpoint = 0
    else:
        yearstring = year1 + str(int(year1) +1)
        startpoint = years.index(yearstring)

    for year in years[startpoint:]:
        teams = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + i +'/?expand=team.stats&season='+year)

        team_name = teams.json()['teams'][0]['name']

        team_stats = teams.json()['teams'][0]['teamStats'][0]['splits'][0]['stat']
        #add a year column and a team name column for filtering later
        team_stats['Year'] = year[-4:]
        team_stats['Team'] = team_name

        df = df.append(team_stats, ignore_index = True)

#Change all non numeric columns to numeric
df['Year'] = pd.to_numeric(df['Year'])
df['powerPlayPercentage'] = pd.to_numeric(df['powerPlayPercentage'])
df['penaltyKillPercentage'] = pd.to_numeric(df['penaltyKillPercentage'])
df['gamesPlayed'] = pd.to_numeric(df['gamesPlayed'])
df['wins'] = pd.to_numeric(df['wins'])
df['losses'] = pd.to_numeric(df['losses'])
df['ot'] = pd.to_numeric(df['ot'])
df['pts'] = pd.to_numeric(df['pts'])
df['ptPctg'] = pd.to_numeric(df['ptPctg'])
df['faceOffWinPercentage'] = pd.to_numeric(df['faceOffWinPercentage'])

#generate league median
for year in df.Year.unique():
    year_avgs = []
    yeardf=df[df['Year']==year]
    for col in yeardf:
        try:
            year_avgs.append(yeardf[col].median())
        except:
            continue
    year_avgs[-1]= 'League Median'
    year_avgs.append(year)
    series = pd.Series(year_avgs, index= df.columns)
    df = df.append(series, ignore_index = True)
