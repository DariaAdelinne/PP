import requests
import time
import json
import os
from abc import ABC, abstractmethod  #importam clasele de baza pentru a defini interfete abstracte
from multiprocessing import Lock  #importam Lock pentru acces sincronizat la fisierul de cache

CACHE_FILE = 'http_cache.json'  #numele fisierului unde vom stoca cache-ul
CACHE_TTL = 3600  #timpul de viata al unei intrari in cache in secunde (1 ora)
LOCK = Lock()  #lock pentru a proteja scrierea concurenta in fisierul de cache

class HttpClient(ABC):  #interfata abstracta
    @abstractmethod
    def get(self, url: str) -> str:  #metoda abstracta pentru a face GET si a returna textul raspunsului
        pass

class RequestsHttpClient(HttpClient):  #implementarea concreta folosind requests
    def get(self, url: str) -> str:
        r = requests.get(url)  #facem cererea HTTP GET catre URL
        r.raise_for_status()   #daca raspunsul nu e 2xx, ridicam exceptie
        return r.text          #returnam continutul raspunsului ca text

class CachingProxy(HttpClient):  #proxy care adauga functionalitate de caching peste un HttpClient
    def __init__(self, real_client: HttpClient):
        self.real_client = real_client  #clientul real care face cererile
        self._load_cache()  #incarcam cache-ul existent din fisier

    def _load_cache(self):  # metoda pentru a incarca datele din fisier
        if os.path.exists(CACHE_FILE):  #verificam daca fisierul de cache exista
            with open(CACHE_FILE, 'r') as f:
                self.cache = json.load(f)  #incarcam dictionarul cache din fisier
        else:
            self.cache = {}  #daca nu exista, initializam cache-ul ca un dictionar gol

    def _save_cache(self):  #metoda  pentru a salva cache-ul in fisier
        with LOCK:  #blocam accesul concurent
            with open(CACHE_FILE, 'w') as f:
                json.dump(self.cache, f)  #serializam dictionarul cache in fisier ca JSON

    def get(self, url: str) -> str:  #implementarea metodei get din interfata
        now = time.time()  #preluam timpul curent ca timestamp
        entry = self.cache.get(url)  #cautam intrarea aferenta URL-ului in cache

        if entry:  #daca exista o intrare in cache extragem timpul la care a fost stocata
            timestamp = entry['timestamp']
            if now - timestamp < CACHE_TTL:  #daca nu a expirat (mai putin de o ora)
                print(f"[Cache] Returnam cache pentru {url}")
                return entry['response']  #returnam raspunsul din cache
            else:
                print(f"[Cache] Intrare expirat pentru {url}")  #cache expirat

        print(f"[Proxy] Fetching {url}")  #logam ca vom face cererea reala
        resp = self.real_client.get(url)  #cererea HTTP reala prin clientul real

        self.cache[url] = {
            'timestamp': now,     #stocam timpul curent
            'response': resp      #si continutul raspunsului
        }
        self._save_cache()  #salvam noile date in fisier
        return resp  #returnam raspunsul nou obtinut

class LoadBalancingStrategy(ABC):  #interfata pentru strategiile de load balancing
    @abstractmethod
    def select(self, clients: list) -> HttpClient:  #alege un client din lista
        pass

class RoundRobinStrategy(LoadBalancingStrategy):  #implementarea round-robin
    def __init__(self): self.index = 0  #indexul clientului curent
    def select(self, clients: list) -> HttpClient:
        client = clients[self.index % len(clients)]  #alegem clientul in mod ciclic
        self.index += 1  #incrementam indexul pentru urmatoarea selectie
        return client

class LoadBalancer:
    def __init__(self, strategy: LoadBalancingStrategy):
        self.strategy = strategy  #strategia de balansare
        self.clients = [CachingProxy(RequestsHttpClient())]  #lista initiala cu un singur client proxy
        self.request_counts = []  #istoric de numar de cereri: fiecare element = [fereastra, count]
        self.window_size = 60  #dimensiunea ferestrei de monitorizare in secunde

    def _current_window(self):
        now = time.time()  #timestamp curent
        return int(now // self.window_size)  #coeficient de fereastra curenta

    def _record_request(self):  #inregistram o cerere in fereastra curenta
        window = self._current_window()
        if not self.request_counts or self.request_counts[-1][0] != window:
            #daca e prima cerere sau trecerea in alta fereastra, cream un nou record
            self.request_counts.append([window, 0])
        self.request_counts[-1][1] += 1  #incrementam contorul pentru fereastra curenta
        #daca avem date din doua ferestre consecutive, comparam
        if len(self.request_counts) >= 2:
            prev = self.request_counts[-2][1]  #cereri in fereastra anterioara
            curr = self.request_counts[-1][1]  #cereri in fereastra curenta
            if prev > 0 and curr >= 10 * prev:  #daca s-a inmultit de 10x
                self._spawn_new_client()  #declansam replicarea

    def _spawn_new_client(self):  #adaugam un nou client proxy
        print("[LoadBalancer] Traffic spike detected: repartizarea cererilor...")
        new_client = CachingProxy(RequestsHttpClient())  #instantiem un nou proxy+client
        self.clients.append(new_client)  #il adaugam in lista
        print(f"[LoadBalancer] Numar instante: {len(self.clients)}")

    def get(self, url: str) -> str:
        self._record_request()  #intai inregistram cererea pentru monitoring
        client = self.strategy.select(self.clients)  #alegem clientul via strategie
        return client.get(url)  #apelam get pe clientul ales si returnam raspunsul

if __name__ == '__main__':
    lb = LoadBalancer(RoundRobinStrategy())  #cream load balancer cu strategie round-robin
    urls = ['https://httpbin.org/get', 'https://api.github.com']  #doua URL-uri de test
    #Simulam 30 de cereri, cate una pe secunda
    for i in range(30):
        u = urls[i % len(urls)]  #alternam intre cele doua URL-uri
        print(f"Cerere {i+1} catre {u}")
        try:
            out = lb.get(u)  #primim raspuns via load balancer
            print(f"— Received {len(out)} chars")  #afisam lungimea raspunsului
        except Exception as e:
            print("ERROR:", e)  #afisam eroarea daca apare
        time.sleep(1)  #asteptam o secunda inainte de urmatoarea cerere
