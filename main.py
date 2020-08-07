import os
import json
import config
import random
import logging
from vk_api import VkApi
from threading import Thread, Lock
from vk_api.exceptions import VkApiError
from vk_api.bot_longpoll import VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType, Event


class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.raw


class Bot:
    def __init__(self):
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.INFO)

        fh = logging.FileHandler(config.log_file)
        formatter = logging.Formatter('%(asctime)s | %(name)s : %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.vk = VkApi(token=config.token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk = self.vk.get_api()

        if not config.two_factor:
            self.user_vk = VkApi(login=config.login, password=config.password)
        else:
            def two_factor(): return input("Write your code: "), True
            self.user_vk = VkApi(config.login, config.password, auth_handler=two_factor)

        self.user_vk.auth()
        self.user_vk = self.user_vk.get_api()

        self.posts_to_do = []
        if os.path.exists(config.exceed_file):
            self.logger.info("Uploading from file")
            try:
                with open(config.exceed_file, 'r') as file:
                    self.posts_to_do = json.load(file)
            except json.JSONDecodeError:
                print("Decoding error, posts are empty now")

        self.exceed_thread = Thread(target=self.post_exceed)

    def start(self):
        self.logger.info("Starting the bot")
        self.exceed_thread.start()
        self.listen()

    def listen(self):
        try:
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and not event.from_me and event.from_user:
                    post_message = self.new_post(event)
                    self.send_message(event.peer_id, post_message)

                elif event.type == VkBotEventType.GROUP_JOIN:
                    self.logger.info(f"New user {event.user_id}")
                    self.send_message(event.peer_id, config.group_join)

                elif event.type == VkBotEventType.GROUP_LEAVE:
                    self.logger.info(f"User {event.user_id} left")
                    self.send_message(event.peer_id, config.group_leave)

        except Exception as exc:
            self.logger.error(exc)

    def send_message(self, where, message, attachments=None):
        self.logger.info(f"Message '{message}' sent to {where} with {attachments}")
        self.vk.messages.send(peer_id=where, message=message,
                              attachments=attachments,
                              random_id=random.randint(0, 100000))

    def post_exceed(self):
        post = None
        while True:
            if not self.posts_to_do:
                continue

            try:
                post = Event(self.posts_to_do.pop())
                self.post(post)
                self.send_message(post.user_id, config.post_successful)

            except Exception as exc:
                if post is not None:
                    self.posts_to_do.append(post)
                print("Posts per day counter exceeded")

            finally:
                self.save()

    def post(self, event):
        attachments = []

        for i in range(0, len(event.attachments), 2):
            attachment_type = event.attachments[f'attach{i + 1}_type']
            attachment = event.attachments[f'attach{i + 1}']
            attachments.append(f"{attachment_type}{attachment}")

        post_id = self.user_vk.wall.post(message=event.text, attachments=attachments, owner_id=config.group_id)
        self.logger.info(f"Post done {post_id['post_id']}")

    def new_post(self, event):
        try:
            self.post(event)
            return config.post_successful

        except Exception as exc:
            if isinstance(exc, VkApiError) and exc.code == 100:
                return config.write_message

            else:
                self.posts_to_do.append(event)
                return config.post_queue.format(len(self.posts_to_do))

    def save(self):
        with open(config.exceed_file, 'w') as file:
            json.dump(self.posts_to_do, file, cls=EventEncoder)
        self.logger.info("Posts are saved!")


if __name__ == '__main__':
    bot = Bot()
    print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(0, 250, 0, """
 _                     _    _                                       _       
| |                   | |  | |                                     | |      
| | ___ __  _   _  ___| | _| | ___  ___ _   _  __ _  __ _ _ __   __| | __ _ 
| |/ / '_ \| | | |/ __| |/ / |/ _ \/ __| | | |/ _` |/ _` | '_ \ / _` |/ _` |
|   <| | | | |_| | (__|   <| |  __/\__ \ |_| | (_| | (_| | | | | (_| | (_| |
|_|\_\_| |_|\__,_|\___|_|\_\_|\___||___/\__,_|\__, |\__,_|_| |_|\__,_|\__,_|
                                               __/ |                        
                                              |___/        
    https://github.com/knucklesuganda   
    https://github.com/knucklesuganda
    https://github.com/knucklesuganda
"""))
    bot.start()
