### Определяет политику, которая будет использовать `Redis` при достижении `maxmemory`.

`Note: LRU — Less Recently Used`

Может иметь одно из значений:

- `volatile-lru`: будут удалены наименее используемые ключи, у которых задан expire
- `allkeys-lru`: будут удалены наименее используемые ключи независимо от expire
- `volatile-random`: удалить случайный ключ с заданным expire
- `allkeys-random`: удалить случайный ключ независимо от expire
- `volatile-ttl`: удалить ключ с наименьшим оставшимся TTL
- `noeviction`: не выполнять очистку вообще, просто возвращать ошибку при операциях записи

# Dialogflow chatbot
The chatbot answers the most frequent user's questions from telegram or VK.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need create environment variables:
- `BOT_TOKEN` from @Bot_father.
- `GOOGLE_APPLICATION_CREDENTIALS` contains "private_key.json". 
How to get json key see below.
- `PRJ_ID` Project ID from Project Info in your google cloud console.
- `TELEGRAM_ID` your telegram id from @userinfobot (type command: "/start").
- `VK_BOT_ID` number XXXXXXXXX from URL of your community: "https://vk.com/clubXXXXXXXXX"
- `VK_TOKEN` your VK community token. How to get vk community token see below.

You need install `requirements.txt`
```    
pip install -r requirements.txt
```


### Create JSON KEY

Create a service account:

- In the Cloud Console, go to the Create service account page.
- Go to Create service account
-> Select a project.
- In the Service account name field, enter a name. The Cloud Console fills in the Service account ID field based on this name.
- In the Service account description field, enter a description. For example, Service account for quickstart.
- Click Create.
- Click the Select a role field.
- Under Quick access, click Basic, then click Owner.

Note: The Role field affects which resources your service account can access in your project. You can revoke these roles or grant additional roles later. In production environments, do not grant the Owner, Editor, or Viewer roles. For more information, see Granting, changing, and revoking access to resources.

- Click Continue.
- Click Done to finish creating the service account.
- Do not close your browser window. You will use it in the next step.
- Create a service account key:
- In the Cloud Console, click the email address for the service account that you created.
- Click Keys.
- Click Add key, then click Create new key.
- Click Create. A JSON key file is downloaded to your computer.
- Click Close.

For more infomation, see [Working with Dialogflow using Python Client](https://medium.com/swlh/working-with-dialogflow-using-python-client-cb2196d579a4).


### Get VK community token

You need:
- create community on the ["control" tab](https://vk.com/groups?tab=admin).
- get vk community token: "Manage" - "API usage" - button "Create token" - checkbox "Allow access to community management" and "Allow access to community messages" - add `VK_TOKEN` in `.env`.
- allow to send message: "Manage" - "Messages" - "Community message" is "Enabled" - type "Greeting message" (for example, "Hello, have you questions?") - button "Save".

### Features vk_bot.py

Note: if you want to work with longpoll `bot_longpoll.py` from [vk_api examples](https://github.com/python273/vk_api/tree/master/examples), you need: "Manage" - "API usage" - "LongPoll" set "Enabled" and select version API `>5.80`.

### Fitting of Dialogflow agent
To fit agent you need run `fit_bot.py`. You can add or modify training phrases in `questions.json` file.