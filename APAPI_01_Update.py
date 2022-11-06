import requests
import json
import configparser
import os

# Setting
config = configparser.ConfigParser()
config.read('APAPI.ini')
# Set api key
APIKEY = os.environ.get('APAPIKEY')
# Set resultstype
RESULTSTYPE = config['Default']['resultstype']
print(f'Results type is {RESULTSTYPE}')
# Election date
ELECTIONDATE = '2022-11-08'

# Get election results

# Senate
# Setting
officeID = 'S'
savefile = config['SaveFile']['senate_update'].replace('datadir', config['Path']['datadir']).replace('TIMESTAMP', str(int(time.time())))
# Request
res = requests.get(
    config['NextRequest']['senate']+f'&apikey={APIKEY}')
result = res.json()
# save update info
config['NextRequest']['senate'] = result['nextrequest'].replace('%', '%%')
# save json
with open(savefile, 'w') as fw:
    json.dump(result, fw)
    
# House
# Setting
officeID = 'H'
savefile = config['SaveFile']['house_update'].replace('datadir', config['Path']['datadir']).replace('TIMESTAMP', str(int(time.time())))
# Request
res = requests.get(
    config['NextRequest']['house']+f'&apikey={APIKEY}')
result = res.json()
# save update info
config['NextRequest']['house'] = result['nextrequest'].replace('%', '%%')
# save json
with open(savefile, 'w') as fw:
    json.dump(result, fw)
    
# Governor
# Setting
officeID = 'G'
savefile = config['SaveFile']['governor_update'].replace('datadir', config['Path']['datadir']).replace('TIMESTAMP', str(int(time.time())))
# Request
res = requests.get(
    config['NextRequest']['governor']+f'&apikey={APIKEY}')
result = res.json()
# save update info
config['NextRequest']['governor'] = result['nextrequest'].replace('%', '%%')
# save json
with open(savefile, 'w') as fw:
    json.dump(result, fw)