import asyncio

async def worker(name: str, queue: asyncio.Queue):
    n = await queue.get()
    total = sum(range(n + 1))
    print(f"{name} a calculat suma 0..{n} = {total}")
    queue.task_done()

async def main():
    queue = asyncio.Queue()

    valori_n = [100, 1000, 10000, 100000]
    for n in valori_n:
        await queue.put(n)

    tasks = [
        asyncio.create_task(worker(f"corutina-{i+1}", queue))
        for i in range(len(valori_n))
    ]

    await queue.join()

    for t in tasks:
        t.cancel()

if __name__ == "__main__":
    asyncio.run(main())
