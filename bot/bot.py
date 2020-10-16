import utils
import vk_api
import threading
import traceback
from config import settings
from vk_api.longpoll import VkLongPoll, VkEventType

print('начата авторизация.')
try:
    vk_session = vk_api.VkApi(token = settings['access_token'])
    longpoll = VkLongPoll(vk_session)
    owner_id = utils.api('account.getProfileInfo')['id']; logged = True
    ru_trigger, en_trigger = settings['ru_trigger'], settings['en_trigger']
except Exception as error:
    print(error); exit()

muted = []

def mainLongPoll():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.from_me:
                    event_object_id, message_id = utils.received_object.id(event), event.message_id
                    text = event.text.lower()

                    if text.startswith(en_trigger + ' +mute') or text.startswith(ru_trigger + ' +мут'):
                        object_id = int(utils.find_id(event, text))
                        if object_id in muted:
                            pass
                        elif object_id not in muted:
                            muted.append(object_id)

                    if text.startswith(en_trigger + ' -mute') or text.startswith(ru_trigger + ' -мут'):
                        object_id = int(utils.find_id(event, text))
                        if object_id in muted:
                            muted.remove(object_id)
                        elif object_id not in muted:
                            pass

                    if text.startswith(en_trigger + ' -admin') or text.startswith(ru_trigger + ' -админ'):
                        object_id = utils.find_id(event, text)
                        utils.api('messages.setMemberRole', member_id = object_id, peer_id = event_object_id, role = 'member')

                    if text.startswith(en_trigger + ' +admin') or text.startswith(ru_trigger + ' +админ'):
                        object_id = utils.find_id(event, text)
                        utils.api('messages.setMemberRole', member_id = object_id, peer_id = event_object_id, role = 'admin')

                    if text.startswith(en_trigger + ' kick') or text.startswith(ru_trigger + ' кик'):
                        event_object_id, event_object_type = utils.received_object.id(event), utils.received_object.type(event)
                        object_id = utils.find_id(event, text)
                        if event_object_type == 'chat.message':
                            utils.api('messages.removeChatUser', chat_id = event_object_id - 2000000000, user_id = object_id)


                if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                    event_object_id, event_object_type = utils.received_object.id(event), utils.received_object.type(event)
                    message_id = event.message_id
                    if event_object_type != 'group.message':
                        if event.user_id in muted:
                            utils.api('messages.delete', message_ids = message_id)


        except:
            utils.api('messages.send', user_id = owner_id, message = traceback.print_exc())

if __name__ == '__main__':
    if logged:
        print('запуск потока.')
        main = threading.Thread(target = mainLongPoll).start()

# [52, 6, 2000000219, 443401774]
# [52, 8, 2000000219, 443401774]