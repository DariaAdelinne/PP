import asyncio

async def worker(name: str, queue: asyncio.Queue):
    # preia o valoare n din coada si calculeaza suma de la 0 la n
    n = await queue.get()
    print(f"{name} a preluat n={n}")
    # calculam suma folosind formula sau iterativ
    total = sum(range(n+1))
    # alternativ: total = n * (n + 1) // 2
    await asyncio.sleep(0)  # yield control pentru a simula concurenta
    print(f"{name}: Suma de la 0 la {n} este {total}")
    queue.task_done()

async def main():
    # cream coada si introducem patru valori diferite pentru n
    q = asyncio.Queue()
    values = [10, 25, 100, 7]
    for v in values:
        await q.put(v)

    # lansam patru corutine care vor prelua fiecare cate o valoare
    tasks = []
    for i in range(1, 5):
        task = asyncio.create_task(worker(f"Worker-{i}", q))
        tasks.append(task)

    # asteptam golirea cozii
    await q.join()

    # asteptam finalizarea tuturor task-urilor
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())