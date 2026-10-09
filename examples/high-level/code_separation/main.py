import os

from openvkbottle import Bot

from .handlers import labelers

# Load token from system environment variable
# https://12factor.net/config
bot = Bot(os.environ["TOKEN"])

for labeler in labelers:
    bot.labeler.load(labeler)

bot.run()
