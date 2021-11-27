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
