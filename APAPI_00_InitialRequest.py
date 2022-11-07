import requests
import json
import configparser
import os
import pandas as pd

# Setting
config = configparser.ConfigParser()
config.read('APAPI.ini')
# Set api key
APIKEY = '8ob3i6tphhraof83cz7wad6mwh'
# Set resultstype
RESULTSTYPE = config['Default']['resultstype']
print(f'Results type is {RESULTSTYPE}')
# Election date
ELECTIONDATE = '2022-11-08'

# Get election results

# Senate
# Setting
officeID = 'S'
savefile = config['SaveFile']['senate'].replace('datadir', config['Path']['datadir'])
# Request
res = requests.get(
    f'https://api.ap.org/v3/elections/{ELECTIONDATE}?apikey={APIKEY}&officeID={officeID}&resultstype={RESULTSTYPE}&winner=X&format=json')
result = res.json()
# save update info
config['NextRequest']['senate'] = result['nextrequest'].replace('%', '%%')

races = result['races']
winners = pd.DataFrame()
for race in races:
    df = pd.DataFrame(race['reportingUnits'][0]['candidates'])
    df['statePostal'] = race['reportingUnits'][0]['statePostal']
    df['stateName'] = race['reportingUnits'][0]['stateName']
    df['raceID'] = race['raceID']
    if 'seatNum' in race.keys():
        df['seatNum'] = race['seatNum']
    winners = pd.concat([winners, df])
if len(winners) == 0:
    pd.DataFrame(columns=['first', 'last', 'party', 'candidateID', 'polID', 'ballotOrder',
       'polNum', 'voteCount', 'electWon', 'winner', 'winnerDateTime',
       'statePostal', 'stateName', 'raceID']).to_csv(savefile, encoding='utf_8_sig', index=False)
else:
    winners.to_csv(savefile, encoding='utf_8_sig', index=False)



# House
# Setting
officeID = 'H'
savefile = config['SaveFile']['house'].replace('datadir', config['Path']['datadir'])
# Request
res = requests.get(
    f'https://api.ap.org/v3/elections/{ELECTIONDATE}?apikey={APIKEY}&officeID={officeID}&resultstype={RESULTSTYPE}&winner=X&format=json')
result = res.json()
# save update info
config['NextRequest']['house'] = result['nextrequest'].replace('%', '%%')

races = result['races']
winners = pd.DataFrame()
for race in races:
    df = pd.DataFrame(race['reportingUnits'][0]['candidates'])
    df['statePostal'] = race['reportingUnits'][0]['statePostal']
    df['stateName'] = race['reportingUnits'][0]['stateName']
    df['raceID'] = race['raceID']
    if 'seatNum' in race.keys():
        df['seatNum'] = race['seatNum']
    winners = pd.concat([winners, df])
if len(winners) == 0:
    pd.DataFrame(columns=['first', 'last', 'party', 'incumbent', 'candidateID', 'polID',
       'ballotOrder', 'polNum', 'voteCount', 'electWon', 'winner',
       'winnerDateTime', 'statePostal', 'stateName', 'raceID', 'seatNum',
       'abbrv', 'middle']).to_csv(savefile, encoding='utf_8_sig', index=False)
else:
    winners.to_csv(savefile, encoding='utf_8_sig', index=False)
    
# # Governor
# # Setting
# officeID = 'G'
# savefile = config['SaveFile']['governor'].replace('datadir', config['Path']['datadir'])
# # Request
# res = requests.get(
#     f'https://api.ap.org/v3/elections/{ELECTIONDATE}?apikey={APIKEY}&officeID={officeID}&resultstype={RESULTSTYPE}&winner=X&format=json')
# result = res.json()
# # save update info
# config['NextRequest']['governor'] = result['nextrequest'].replace('%', '%%')

# races = result['races']
# winners = pd.DataFrame()
# for race in races:
#     df = pd.DataFrame(race['reportingUnits'][0]['candidates'])
#     df['statePostal'] = race['reportingUnits'][0]['statePostal']
#     df['stateName'] = race['reportingUnits'][0]['stateName']
#     df['raceID'] = race['raceID']
#     if 'seatNum' in race.keys():
#         df['seatNum'] = race['seatNum']
#     winners = pd.concat([winners, df])
# winners.to_csv(savefile, encoding='utf_8_sig', index=False)
    
# # Save updated setting
# with open('APAPI.ini', 'w') as configfile:
#     config.write(configfile)