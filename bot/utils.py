import requests
from config import settings

def api(method, token = settings["access_token"], **kwargs):
    api_url, version = "https://api.vk.com/method/", 5.103
    url = f'{api_url}{method}?access_token={token}&v={version}'
    keys = list(kwargs.keys())
    for index in range(0, len(keys)):
        url = url + f'&{keys[index]}={kwargs[keys[index]]}'
    json_response = requests.get(url).json()
    try:
        return json_response['response']
    except KeyError:
        print('error code - ' + str(json_response['error']['error_code']))
        print(json_response['error']['error_msg'])
        return 'error.'
class received_object:
    def __init__(self):
        self.from_group = None
        self.group_id = None
        self.chat_id = None
        self.user_id = None
        self.from_chat = None
        self.from_user = None

    def id(event):
        if event.from_chat:
            return 2000000000 + int(event.chat_id)
        elif event.from_user:
            return event.user_id
        elif event.from_group:
            return '-' + str(event.group_id)
    def type(event):
        if event.from_chat:
            return 'chat.message'
        elif event.from_user:
            return 'user.message'
        elif event.from_group:
            return 'group.message'

def find_id(event, string):
    one, two = string.find('['), string.find('|')
    if -1 not in [one, two] and one < two:
        return string[one + 1:two].replace('id', '')
    if -1 in [one, two] or one > two:
        one, two = string.find('http'), string.find('https')
        if -1 not in [one, two]:
            while string.find('/') != -1:
                string = string.partition('/')[2]
            return api('users.get', user_ids = string)[0]['id']
        if -1 in [one, two]:
            if event.raw[6].get('mentions') == None:
                return 'undefinded'
            elif not event.raw[6].get('mentions') is None:
                return event.raw[6].get('mentions')[0]


