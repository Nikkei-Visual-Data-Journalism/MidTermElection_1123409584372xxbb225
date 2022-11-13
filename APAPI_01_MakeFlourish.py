import pandas as pd

# Import Templates
map_house = pd.read_csv('Flourish_templates/map_house.csv', encoding='utf_8_sig', dtype=object)
map_senate = pd.read_csv('Flourish_templates/map_senate.csv', encoding='utf_8_sig', dtype=object)
bar_house = pd.read_csv('Flourish_templates/bar_house.csv', encoding='utf_8_sig', dtype=object)
bar_senate = pd.read_csv('Flourish_templates/bar_senate.csv', encoding='utf_8_sig', dtype=object)

# Import winners data
house = pd.read_csv('APAPI/electionResultsWinners_house.csv', encoding='utf_8_sig', dtype=object)
senate = pd.read_csv('APAPI/electionResultsWinners_senate.csv', encoding='utf_8_sig', dtype=object)

# Import race ids
raceID_house = pd.read_csv('raceID_house.csv', encoding='utf_8_sig', dtype=object)['raceID'].to_list()
raceID_senate = pd.read_csv('raceID_senate.csv', encoding='utf_8_sig', dtype=object)['raceID'].to_list()
house = house[house.raceID.isin(raceID_house)].copy()
senate = senate[senate.raceID.isin(raceID_senate)].copy()

# Make map_house
if len(house) > 0:
    _dict = {'Dem':'民主党', 'GOP':'共和党'}
    _dict2 = map_house.set_index('districtID')['district'].to_dict()
    df = house.copy()
    df['districtID'] = df['statePostal'].astype(str) + df['seatNum'].astype(str).str.zfill(2)
    df['政党'] = df['party'].apply(lambda x: _dict[x] if x in _dict.keys() else 'その他')
    map_house = pd.merge(map_house[['geometry', 'districtID']], df[['districtID', '政党']], on='districtID', how='left').fillna('残り')
    map_house['district'] = map_house['districtID'].apply(lambda x: _dict2[x])
map_house.to_csv('Flourish/map_house.csv', encoding='utf_8_sig', index=False)

# Make map_senate
if len(senate) > 0:
    for i, row in map_senate[map_senate['議席']=='改選'].iterrows():
        t_df = senate[senate.raceID==row.raceID].copy()
        if len(t_df) == 1:
            map_senate.loc[i, '結果'] = _dict[t_df.iloc[0].party] if t_df.iloc[0].party in _dict.keys() else 'その他'
map_senate.to_csv('Flourish/map_senate.csv', encoding='utf_8_sig', index=False)

# Make bar_house
if len(house) > 0:
    _dict = {'Dem':'民主党', 'GOP':'共和党'}
    df = house.copy()
    df.party = df.party.apply(lambda x: _dict[x] if x in _dict.keys() else 'その他')
    result = df.party.value_counts().to_dict()
    for c in ['民主党', 'その他', '共和党']:
        if c not in result.keys():
            result[c] = 0
    result['民主党'] += 
    for c in ['民主党', 'その他', '共和党']:
        bar_house.iloc[0][c] = result[c]
    bar_house.iloc[0]['残り'] = 435 - sum(result.values())
bar_house.to_csv('Flourish/bar_house.csv', encoding='utf_8_sig', index=False)

# Make bar_senate
if len(senate) > 0:
    _dict = {'Dem':'民主党', 'GOP':'共和党'}
    df = senate.copy()
    df.party = df.party.apply(lambda x: _dict[x] if x in _dict.keys() else 'その他')
    result = df.party.value_counts().to_dict()
    for c in ['民主党', 'その他', '共和党']:
        if c not in result.keys():
            result[c] = 0
    result['共和党'] += 1
    for c in ['民主党', 'その他', '共和党']:
        bar_senate.iloc[0][c] = result[c]
    bar_senate.iloc[0]['残り'] = 35 - sum(result.values())
bar_senate.to_csv('Flourish/bar_senate.csv', encoding='utf_8_sig', index=False)
