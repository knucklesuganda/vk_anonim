# vk_anonim

Anonymous posts bot for VK.
===========

Uses vk.com social network API. 

## How to register and create a group in vk.com
1) Register in vk.com social network.
2) Go to communities https://vk.com/groups
3) Press create community https://vk.com/groups?w=groups_create
4) Follow the instructions and create your community
5) Open your community page and go to manage
6) Go to API usage and create a new token(save it)
7) Go to long poll API, turn it on, and choose the version you like ```The bot was created on the version 5.101 and API can change, thus, disrupting the bot in the future```
8) Go to event types of Longpoll API and tick everything
9) Go to messages in your manage section and enable community messages
10) Go to bot settings near your community messages section and choose Enabled
11) Save everything
## How to set up your bot 
1) Execute: ```pip install -r requirements.txt```
2) Go to ```config.py```. That file helps you to set up your bot and custom messages.
```python
token = ""  # paste the group token you gained at the 6th step.
login = ""  # paste the phone number you used when you registered
password = ""  # paste your password you used when you registered
two_factor = True  # if you enabled two-factor auth, leave True, otherwise False
group_id = -0  # group id paste your group id here. To find it, go to your community page(https://vk.com/club0000000) and copy only the numbers in the URL.
log_file = 'file.log'  # File used for logs, if you experience crashes, go here and find the problem. You can change the name if you want to.
exceed_file = "posts.json"  # Vk has a limited amount of posts per day, if your users send you more than the limit says, all posts will be saved here and posted the next day.

# messages
# These messages are used to signalize the user, you can see their translations after the # sign. If you want to change them, you can do it.

write_message = "Напишите сообщение чтобы мы могли сделать пост" # Write the message, so we can post it
post_successful = f"Ваш пост уже в нашей группе!" # Your post is already in our group!
post_queue = f"Вы в очереди на пост, перед вами: {0}" # You are queued, your number is {0}
group_join = f"Напишите сообщение чтобы сделать анонимный пост" # Write the message, to create an anonymous post.
group_leave = f"Возвращайтесь!" # Return to our group!
# messages
```

## How to run your bot
1) Execute ```python main.py```


