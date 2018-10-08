import requests
import re

from .exceptions import FutError

# config
rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/config/config.json').json()
auth_url = rc['authURL']
pin_url = rc['pinURL']  # TODO: urls in dict?
client_id = rc['eadpClientId']
fun_captcha_public_key = rc['funCaptchaPublicKey']

# dynamic hex numbers:
rc = requests.get('https://www.easports.com/de/fifa/ultimate-team/web-app/').text

resourceRoot = re.search('resourceRoot\s*=\s*"(.+?)\";', rc).group(1)
resourceBase = re.search('resourceBase\s*=\s*"(.+?)\";', rc).group(1)
guid = re.search('guid\s*=\s*"(.+?)\";', rc).group(1)
year = re.search('year\s*=\s*"(.+?)\";', rc).group(1)


# remote config - should be refresh every x seconds
rc = requests.get('https://www.easports.com/fifa/ultimate-team/web-app/content/7D49A6B1-760B-4491-B10C-167FBC81D58A/2019/fut/config/companion/remoteConfig.json').json()

if rc['pin'] != {"b": True, "bf": 500, "bs": 10, "e": True, "r": 3, "rf": 300}:
    print('>>> WARNING: ping variables changed: %s' % rc['pin'])

if rc['futweb_maintenance']:
    raise FutError('Futweb maintenance, please retry in few minutes.')

itemsPerPage = dict()
itemsPerPage = rc['itemsPerPage']
# nasty hack but it's better than parsing big js file
itemsPerPage['transferMarket'] += 1
itemsPerPage['club'] = 91  # ea, please don't troll us :-)

# TODO: read sku's from https://utas.mob.v1.fut.ea.com/ut/shards/v2

# TODO: card info url not found yet
card_info_url = 'https://fifa19.content.easports.com/fifa/fltOnlineAssets/7D49A6B1-760B-4491-B10C-167FBC81D58A/2019/fut/items/web/'  # TODO: get hash from somewhere, dynamic year
# TODO: could be nice to add locals on startup
messages_url = 'https://www.easports.com/fifa/ultimate-team/web-app/loc/en_US.json'  # TODO: needs to base64 decoded.

