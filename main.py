import discord
from discord import Webhook, RequestsWebhookAdapter
import requests
from datetime import datetime, timedelta
import os

def cronjob():

    url = "https://api.opensea.io/api/v1/events"

    # load discord channel URL
    wh_url = os.environ.get('CHANNEL_URL')
    webhook = Webhook.from_url(wh_url, adapter=RequestsWebhookAdapter())

    # the first mint
    contract = "0x0E892Bff0658b93B326E14d4558Ce25a642676DA"

    OPENSEA_SHARED_STOREFRONT_ADDRESS = '0x495f947276749Ce646f68AC8c248420045cb7b5e'

    print('Checking contract {0} for new sales'.format(contract))

    # load Opensea API key
    opensea_api_key = os.environ.get('OS_API_KEY')

    # get current time in utc time zone
    ct = datetime.utcnow()
    # specify time range
    dt = timedelta(minutes = 30)
    pt = ct - dt
    # create string for opensea
    pts = str(pt)
    ostime = pts.split(' ')[0] + 'T' + pts.split(' ')[1]

    querystring = {"asset_contract_address": contract,
                   "event_type": "successful",
                   "only_opensea": "true",
                   "occurred_after": ostime,
                   "offset":0,
                   "limit":"50"}

    headers = {"Accept": "application/json",
               "X-API-KEY": opensea_api_key}

    response = requests.request("GET", url, headers=headers, params=querystring)

    # if response.status_code != 200:
    #     print('error')
    #     break

    # getting sales data
    sales_data = response.json()['asset_events']

    # if sales_data == []:
    #     break

    for j in range(len(sales_data)):

        name = sales_data[j]['asset']['name']
        try:
            buyer = sales_data[j]['winner_account']['user']['username']
        except:
            buyer = 'Anon'
        buyer_address = sales_data[j]['winner_account']['address']
        total_price = sales_data[j]['total_price']
        try:
            seller = sales_data[j]['seller']['user']['username']
        except:
            seller = 'Anon'
        seller_address = sales_data[j]['seller']['address']
        payment_symbol = sales_data[j]['payment_token']['symbol']
        payment_decimals = sales_data[j]['payment_token']['decimals']
        payment_USD = sales_data[j]['payment_token']['usd_price']
        timestamp = sales_data[j]['transaction']['timestamp']
        tx_hash = sales_data[j]['transaction']['transaction_hash']

        price_eth = float(total_price) / 10**(payment_decimals)
        price_usd = price_eth * float(payment_USD)

        print('Buyer: ', buyer, ' ', buyer_address)
        print('Seller: ', seller, ' ', seller_address)
        print('Price: {0} {1}'.format(price_eth, payment_symbol))
        print('Price: $', price_usd)
        print('Timestamp: ', timestamp)
        print('Tx Hash: ', tx_hash)

        desc = 'Price: {0} {1}, (${2:.2f})'.format(price_eth, payment_symbol, price_usd)
        embedVar = discord.Embed(title = name + ' Sold!', description = desc, color = 0x00ff00)
        embedVar.add_field(name = 'Buyer', value = '{0} \n {1}'.format(buyer, buyer_address), inline = False)
        embedVar.add_field(name = 'Seller', value = '{0} \n {1}'.format(seller, seller_address), inline = False)

        webhook.send(embed = embedVar)

