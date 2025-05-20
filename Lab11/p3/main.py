import threading
import queue

class ThreadPool:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.tasks = queue.Queue()
        self.results = [] #lista cu rezultate
        self._alive = True #flag pentru thread uri
        self.threads = [] #lista cu thread urile pornite
        for _ in range(num_workers): #creaza num_workers thread uri
            t = threading.Thread(target=self._worker, daemon=True) # dameon=true -> thread urile se pot opri daca se termina programul principal
            t.start()
            self.threads.append(t)

    def _worker(self):
        while self._alive:
            try:
                func, items, start_idx = self.tasks.get(timeout=0.1) #incearca sa preia o sarcina 
            except queue.Empty: #daca coada e goala continua sa astepte
                continue
            for offset, item in enumerate(items): #aplica func pe fiecare element din items si pune rezultatul in self.results la pozitia corecta
                self.results[start_idx + offset] = func(item)
            self.tasks.task_done() #parhceaza sarcina ca fiind completa

    def map(self, func, iterable):
        items = list(iterable) #transforma iterable intr o lista si retine dimeansiunea
        n = len(items)
        self.results = [None] * n #initializam lista de rezultate

        base, rem = divmod(n, self.num_workers) #calculeaza cate elemente va prelcra fiecare thread
        start = 0
        for i in range(self.num_workers): #rupe lista in bucat, pune fiecare sarcina in coada si retine pozitia in lista 
            size = base + (1 if i < rem else 0)
            if size == 0:
                break
            chunk = items[start:start+size]
            self.tasks.put((func, chunk, start))
            start += size

        self.join() 
        return self.results

    def join(self): #asteapta sa se termine toate sarcinile
        self.tasks.join()

    def terminate(self): #salveaza _alive pe false 
        self._alive = False
        while True: #goleste coada daca mai sunt sarcini neprocesate
            try:
                self.tasks.get_nowait()
                self.tasks.task_done()
            except queue.Empty:
                break
        for t in self.threads: #asteapta ca toate firele sa se termine
            t.join()

    def close(self):
        self.terminate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

if __name__ == "__main__":
    import time

    def square(x):
        return x * x

    data = list(range(1, 11))
    with ThreadPool(4) as pool: #creeaza pool cu 4 thread uri
        start = time.perf_counter() #masoara timpul in care sqaure este aplicat fiecarui element din lista
        result = pool.map(square, data)
        end = time.perf_counter()

    print("Rezultat:", result)
    print(f"Timp: {end - start:.6f} sec")
