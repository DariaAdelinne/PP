import asyncio

async def worker(name: str, queue: asyncio.Queue):
    n = await queue.get() #asteapta pana cand poate prelua un element din coada
    total = sum(range(n + 1))
    print(f"{name} a calculat suma 0..{n} = {total}") #afiseaza rezultatul impreuna cu numele corutinei
    queue.task_done()

async def main():
    queue = asyncio.Queue()

    valori_n = [100, 1000, 10000, 100000]
    for n in valori_n:
        await queue.put(n)

    tasks = [ #cream o ista de corutine,una pentru fiecare valoare
        asyncio.create_task(worker(f"corutina-{i+1}", queue)) #lanseaza in executie
        for i in range(len(valori_n))
    ]

    await queue.join() #asteapta pana cand toate sarcinile din coada s au terminat

    for t in tasks:
        t.cancel() #anulam toate corutinele ca sa nu ramana in asteptare

if __name__ == "__main__":
    asyncio.run(main())
