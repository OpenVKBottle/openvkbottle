import os

from openvkbottle.bot import Bot, Message
from openvkbottle.dispatch.handlers import MessageReplyHandler
from openvkbottle.dispatch.rules.base import FuncRule, TextRule
from openvkbottle.tools import WaiterMachine

bot = Bot(os.environ["TOKEN"])
wm = WaiterMachine()


@bot.on.message(text="/greeting")
async def greeting(message: Message):
    await message.answer("Как тебя зовут?")
    m, _ = await wm.wait(
        bot.on.message_view,
        message,
        exit=MessageReplyHandler("Хорошо!", TextRule("/exit"), as_reply=True),
    )
    await message.answer(f"Привет, {m.text.capitalize()}! Будем знакомы.")


@bot.on.message(text="/expiring")
async def expiring(message: Message):
    await message.answer("Напиши палиндром, у тебя 10 секунд!")
    await wm.wait(
        bot.on.message_view,
        message,
        FuncRule(lambda m: m.text == m.text[::-1]),
        default=MessageReplyHandler("Это не палиндром!", as_reply=True),
        expiration=10,
    )
    await message.answer("Отличный палиндром!")


bot.run()
