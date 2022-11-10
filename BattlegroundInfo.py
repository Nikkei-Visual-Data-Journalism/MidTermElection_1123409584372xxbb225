import pandas as pd
import requests

raceID_house = pd.read_csv('raceID_house.csv', encoding='utf_8_sig', dtype=object)
raceID_senate = pd.read_csv('raceID_senate.csv', encoding='utf_8_sig', dtype=object)

# Senate
ELECTIONDATE ='2022-11-08'
OFFICEID = 'S'
res = requests.get(
    f'https://api.ap.org/v3/elections/{ELECTIONDATE}?apikey={APIKEY}&officeID={OFFICEID}&resultstype=l&format=json')

races = res.json()['races']
races = [race for race in races if race['raceID'] in raceID_senate.raceID.to_list()]

for race in races:
    race['statePostal'] = race['reportingUnits'][0]['statePostal']
    candidates = race['reportingUnits'][0]['candidates']
    race['voteCount_Total'] = sum([c['voteCount'] for c in candidates])
    if len([c for c in candidates if c['party']=='GOP'])==1 and len([c for c in candidates if c['party']=='Dem'])==1:
        candidate_GOP = [c for c in candidates if c['party']=='GOP'][0]
        candidate_Dem = [c for c in candidates if c['party']=='Dem'][0]
        race['candidate_GOP'] = candidate_GOP['first'] + ' ' + candidate_GOP['last']
        race['candidate_Dem'] = candidate_Dem['first'] + ' ' + candidate_Dem['last']
        race['voteCount_GOP'] = candidate_GOP['voteCount']
        race['voteCount_Dem'] = candidate_Dem['voteCount']
        race['voteCount_Total'] = sum([c['voteCount'] for c in candidates])
result = pd.DataFrame(races)
result['votePct_GOP'] = result['voteCount_GOP'] / result['voteCount_Total'] * 100
result['votePct_Dem'] = result['voteCount_Dem'] / result['voteCount_Total'] * 100

result = result[(result.raceCallStatus=='Too Early to Call')|(result.statePostal=='GA')]
result = result[(~result.voteCount_GOP.isna())]

result[['statePostal', 'seatNum', 'eevp', 'voteCount_Total', 'candidate_GOP', 'voteCount_GOP', 'votePct_GOP', 'candidate_Dem', 'voteCount_Dem', 'votePct_Dem']].to_csv(
    'Flourish/votePct_senate.csv', encoding='utf_8_sig', index=False
)

# House
ELECTIONDATE ='2022-11-08'
OFFICEID = 'H'
res = requests.get(
    f'https://api.ap.org/v3/elections/{ELECTIONDATE}?apikey={APIKEY}&officeID={OFFICEID}&resultstype=l&format=json')

races = res.json()['races']
races = [race for race in races if race['raceID'] in raceID_house.raceID.to_list()]

for race in races:
    race['statePostal'] = race['reportingUnits'][0]['statePostal']
    candidates = race['reportingUnits'][0]['candidates']
    race['voteCount_Total'] = sum([c['voteCount'] for c in candidates])
    if len([c for c in candidates if c['party']=='GOP'])==1 and len([c for c in candidates if c['party']=='Dem'])==1:
        candidate_GOP = [c for c in candidates if c['party']=='GOP'][0]
        candidate_Dem = [c for c in candidates if c['party']=='Dem'][0]
        race['candidate_GOP'] = candidate_GOP['first'] + ' ' + candidate_GOP['last']
        race['candidate_Dem'] = candidate_Dem['first'] + ' ' + candidate_Dem['last']
        race['voteCount_GOP'] = candidate_GOP['voteCount']
        race['voteCount_Dem'] = candidate_Dem['voteCount']
        race['voteCount_Total'] = sum([c['voteCount'] for c in candidates])
result = pd.DataFrame(races)
result['votePct_GOP'] = result['voteCount_GOP'] / result['voteCount_Total'] * 100
result['votePct_Dem'] = result['voteCount_Dem'] / result['voteCount_Total'] * 100

result = result[(result.raceCallStatus=='Too Early to Call')]
result = result[(~result.voteCount_GOP.isna())]

result[['statePostal', 'seatNum', 'eevp', 'voteCount_Total', 'candidate_GOP', 'voteCount_GOP', 'votePct_GOP', 'candidate_Dem', 'voteCount_Dem', 'votePct_Dem']].to_csv(
    'votePct_house.csv', encoding='utf_8_sig', index=False
)