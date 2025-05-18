import threading
import queue

class ThreadPool:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.tasks = queue.Queue()
        self.results = []
        self._alive = True
        self.threads = []
        for _ in range(num_workers):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            self.threads.append(t)

    def _worker(self):
        while self._alive:
            try:
                func, items, start_idx = self.tasks.get(timeout=0.1)
            except queue.Empty:
                continue
            for offset, item in enumerate(items):
                self.results[start_idx + offset] = func(item)
            self.tasks.task_done()

    def map(self, func, iterable):
        items = list(iterable)
        n = len(items)
        self.results = [None] * n

        base, rem = divmod(n, self.num_workers)
        start = 0
        for i in range(self.num_workers):
            size = base + (1 if i < rem else 0)
            if size == 0:
                break
            chunk = items[start:start+size]
            self.tasks.put((func, chunk, start))
            start += size

        self.join()
        return self.results

    def join(self):
        self.tasks.join()

    def terminate(self):
        self._alive = False
        while True:
            try:
                self.tasks.get_nowait()
                self.tasks.task_done()
            except queue.Empty:
                break
        for t in self.threads:
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
    with ThreadPool(4) as pool:
        start = time.perf_counter()
        result = pool.map(square, data)
        end = time.perf_counter()

    print("Rezultat:", result)
    print(f"Timp: {end - start:.6f} sec")
