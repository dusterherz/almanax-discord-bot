import os
import asyncio
import discord
import imgkit
from datetime import timedelta, datetime, date

CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))
BOT_TOKEN = os.environ.get('BOT_TOKEN')


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print('------')
    
    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID) # The channel id that we want the bot to send message
        print('Background task started')
        print('------')
        while not self.is_closed():
            # Get image from Dofus Almanax Widget (https://almanax.ordredevlad.fr/)
            img_options = {
                'format': 'jpg',
                'encoding': "UTF-8",
                'crop-w': '312',
                'crop-h': '192',
                'crop-x': '8',
                'crop-y': '8',
            }
            img_path = f'almanax-{date.today().strftime("%d-%m-%Y")}.jpg'
            imgkit.from_url('https://almanax.ordredevlad.fr/widget.php?lang=fr&type=full&slide=5&theme=taktik', img_path, options=img_options)

            # Send image to Discord
            print('Send a new Almanax day')
            file = discord.File(img_path)
            await channel.send(file=file)

            # Delete img file
            os.remove(img_path)

            # Wait until midnight for next message
            now = datetime.now()
            tommorrow = now + timedelta(days=1)
            duration = tommorrow.replace(hour=0, minute=0, second=0) - now
            print(f'Waiting {duration.total_seconds()} seconds.')
            await asyncio.sleep(duration.total_seconds())


client = MyClient()
client.run(BOT_TOKEN)
