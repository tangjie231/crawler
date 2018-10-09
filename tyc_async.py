import aiohttp
import asyncio
import requests
import datetime


async def get_content(num, session):
    async with session.get("https://up.daojia.com") as resp:
        print('now run', num)
        print(resp.status)
        print(await resp.text())


def get_content2(num, session):
    with session.get("https://up.daojia.com") as resp:
        print('now run', num)
        print(resp.status_code)
        print(resp.text)


async def run():
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(1, 20):
            tasks.append(get_content(i, session))

        return await asyncio.gather(*tasks)


if __name__ == '__main__':
    session2 = requests.session()

    begin1 = datetime.datetime.now()
    for i in range(1, 20):
        get_content2(i, session2)

    end1 = datetime.datetime.now()
    sync_take_time = (end1 - begin1).microseconds

    session2.close()

    begin = datetime.datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    end = datetime.datetime.now()

    print("======take time========", sync_take_time)
    print("======async take time========", (end - begin).microseconds)
