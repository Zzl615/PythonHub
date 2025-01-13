import asyncio
import random

async def job(name):
    s_time = random.randint(1, 5)
    print(f"{name} sleeping for {s_time} seconds")
    await asyncio.sleep(s_time)

async def main():
    tasks = [
        asyncio.create_task(job(name=index), name=index)
        for index in range(1, 5)
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # print(f"The first task completed was {pending}")

    # print(f"The first task completed was {done.pop()}")

    for item in done.union(pending):
        print(f"The first task completed was {item.get_name()}")

asyncio.run(main())