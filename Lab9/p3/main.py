import requests
import time
import json
import os
from abc import ABC, abstractmethod
from multiprocessing import Process, Lock

CACHE_FILE = 'http_cache.json'
CACHE_TTL = 3600  # 1 oră în secunde
LOCK = Lock()

# ---------- HttpClient Interface ----------
class HttpClient(ABC):
    @abstractmethod
    def get(self, url: str) -> str:
        pass

# ---------- Concrete Client ----------
class RequestsHttpClient(HttpClient):
    def get(self, url: str) -> str:
        r = requests.get(url)
        r.raise_for_status()
        return r.text

# ---------- Caching Proxy ----------
class CachingProxy(HttpClient):
    def __init__(self, real_client: HttpClient):
        self.real_client = real_client
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def _save_cache(self):
        with LOCK:
            with open(CACHE_FILE, 'w') as f:
                json.dump(self.cache, f)

    def get(self, url: str) -> str:
        now = time.time()
        entry = self.cache.get(url)
        # Verificare cache
        if entry:
            timestamp = entry['timestamp']
            if now - timestamp < CACHE_TTL:
                print(f"[Cache] Returnăm cache pentru {url}")
                return entry['response']
            else:
                print(f"[Cache] Intrare expirat pentru {url}")
        # Fetch real
        print(f"[Proxy] Fetching {url}")
        resp = self.real_client.get(url)
        # Actualizăm cache
        self.cache[url] = {
            'timestamp': now,
            'response': resp
        }
        self._save_cache()
        return resp

# ---------- Load Balancing Strategy ----------
class LoadBalancingStrategy(ABC):
    @abstractmethod
    def select(self, clients: list) -> HttpClient:
        pass

class RoundRobinStrategy(LoadBalancingStrategy):
    def __init__(self): self.index = 0
    def select(self, clients: list) -> HttpClient:
        client = clients[self.index % len(clients)]
        self.index += 1
        return client

# ---------- Load Balancer with Monitoring ----------
class LoadBalancer:
    def __init__(self, strategy: LoadBalancingStrategy):
        self.strategy = strategy
        self.clients = [CachingProxy(RequestsHttpClient())]
        self.request_counts = []  # list de perechi (timestamp_window_start, count)
        self.window_size = 60  # secunde

    def _current_window(self):
        now = time.time()
        return int(now // self.window_size)

    def _record_request(self):
        window = self._current_window()
        if not self.request_counts or self.request_counts[-1][0] != window:
            self.request_counts.append([window, 0])
        self.request_counts[-1][1] += 1
        # dacă avem doi timpi în listă, verificăm raport
        if len(self.request_counts) >= 2:
            prev = self.request_counts[-2][1]
            curr = self.request_counts[-1][1]
            if prev > 0 and curr >= 10 * prev:
                self._spawn_new_client()

    def _spawn_new_client(self):
        print("[LoadBalancer] Traffic spike detected: repartizarea cererilor...")
        # Clonăm încă un client (în realitate, am porni un nou proces/instanță)
        new_client = CachingProxy(RequestsHttpClient())
        self.clients.append(new_client)
        print(f"[LoadBalancer] Număr instanțe: {len(self.clients)}")

    def get(self, url: str) -> str:
        self._record_request()
        client = self.strategy.select(self.clients)
        return client.get(url)

# ---------- Exemplu de utilizare ----------
if __name__ == '__main__':
    lb = LoadBalancer(RoundRobinStrategy())
    urls = ['https://httpbin.org/get', 'https://api.github.com']
    # Simulăm 30 de cereri
    for i in range(30):
        u = urls[i % len(urls)]
        print(f"Cerere {i+1} către {u}")
        try:
            out = lb.get(u)
            print(f"— Received {len(out)} chars")
        except Exception as e:
            print("ERROR:", e)
        time.sleep(1)
