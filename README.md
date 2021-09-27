# Discord-Opensea-Sales-Bot

This project displays Opensea sales information in Discord.

## Description

All code is written in Python. This repository is set up to be deployed on Heroku.

1. The first step is to set up a webhook in your Discord server. Go to 'server settings-integrations' and click on webhooks. After creating the webhook you need to 'Copy Webhook URL'. The webhook URL will be used later and provides location for the bot messages.

2. Clone the git repository to your machine. The contract address that is being tracked is hard-coded into 'main.py'. Change this address to the contract address you wish to track.

3. Deploy the project to Heroku. I followed these steps to deploy onto Heroku: https://devcenter.heroku.com/articles/getting-started-with-python After you get set up, you need to add the Webhook URL into Heroku as a configuration variable. Go to 'Settings-Config Vars'. For KEY put CHANNEL_URL and for VALUE copy in the webhook URL.

If you have any questions, you can find me on Twitter @victorbs_dfs
