import os
import asyncio
import discord
import imgkit
from datetime import timedelta, datetime, date
import logging

CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))
BOT_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO, filename='log', filemode='a+', datefmt='%Y-%m-%d %H:%M:%S', format='%(levelname)s: %(asctime)s - %(message)s')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        logging.info('Logged in as')
        logging.info(self.user.name)
        logging.info('------')
    
    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID) # The channel id that we want the bot to send message
        logging.info('Background task started')
        logging.info('------')
        while not self.is_closed():
            logging.info('Preparing a new almanax')
            img_options = {
                'format': 'jpg',
                'encoding': "UTF-8",
                'crop-w': '455',
                'crop-h': '250',
                'crop-x': '250',
                'crop-y': '545',
                'user-style-sheet': 'hide.css'
            }
            almanax_date = datetime.now() + timedelta(hours=3)
            string_date = almanax_date.strftime("%Y-%m-%d")
            img_path = f'almanax-{string_date}.jpg'
            imgkit.from_url(f'http://www.krosmoz.com/fr/almanax/{string_date}', img_path, options=img_options)

            # Send image to Discord
            logging.info('Send a new Almanax day')
            file = discord.File(img_path)
            await channel.send(file=file)

            # Delete img file
            os.remove(img_path)

            # Wait until midnight for next message
            duration = datetime.now().replace(hour=23, minute=0, second=0) + timedelta(days=1) - datetime.now()
            logging.info(f'Waiting {duration.total_seconds()} seconds.')
            await asyncio.sleep(duration.total_seconds())
        logging.info('Closed connection')


client = MyClient()
client.run(BOT_TOKEN)

