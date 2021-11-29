# NHL Stats App
This app is live at: https://nhltrends.herokuapp.com/

app.py is the deployed application file

data-collection.py contains the script used to generate the dataframe used in app.py.  It involves hundreds of API Calls to the NHL api, and only needs to be updated once per season, so a csv is generated instead of making the calls each time the app is opened
