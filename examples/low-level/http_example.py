import asyncio

from openvkbottle.http import AiohttpClient


async def main():
    http = AiohttpClient()
    print(await http.request_text("https://google.com"))
    await http.close()


asyncio.run(main())
