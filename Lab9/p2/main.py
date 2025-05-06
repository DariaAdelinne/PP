from abc import ABC, abstractmethod 

class Observer(ABC):  #serveste ca baza pentru toate clasele
    @abstractmethod
    def update(self, *args, **kwargs):  #metoda apelata la notificare
        pass

class Observable:    #mentine o lista de observatori
    def __init__(self):
        self._observers = []  #lista de observatori 

    def attach(self, observer: Observer):  #atasare observator
        self._observers.append(observer)

    def detach(self, observer: Observer):  #detasare observator
        self._observers.remove(observer)

    def notify_all(self, *args, **kwargs):  #notificare tuturor observatorilor
        for obs in self._observers:
            obs.update(*args, **kwargs)

class DisplayObserver(Observer):  #actualizeaza afisajul cu suma introdusa
    def update(self, money: int):
        print(f"[Display] Suma introdusa: {money} bani")

class ChoiceObserver(Observer):  #selectia produsului
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def update(self, product_name: str, price: int):
        print(f"[Choice] A fost selectat produsul: {product_name} (pret {price} bani)")
        #trimitem eveniment pentru validarea tranzactiei
        self.vending_machine.proceed_to_checkout(product_name, price)

class TakeMoneySTM(Observable):  #automat pentru introducere bani
    class State(ABC):  
        def __init__(self, machine):
            self.machine = machine  #referinta la automat
        @abstractmethod
        def on_event(self, event, value=None):  #procesare eveniment
            pass

    class WaitingForClient(State):  #stare initiala: astept client
        def on_event(self, event, value=None):
            if event == 'client_arrived':  #daca clientul a ajuns
                print("Client ajuns. Astept inserare bani.")
                return self.machine.insert_state  #trecem in starea de inserare
            return self  #altfel ramanem in acelasi state

    class InsertMoney(State):  #stare in care primim bani
        def on_event(self, event, value=None):
            if event == 'insert_coin':  #la inserare moneda
                self.machine.money += value  #actualizam suma
                self.machine.notify_all(self.machine.money)  #notificam display-ul
                return self  #ramanem in aceeasi stare
            return self  #daca alt eveniment, ignora

    def __init__(self):
        super().__init__()
        self.wait_state = TakeMoneySTM.WaitingForClient(self)  #instanta stare asteptare
        self.insert_state = TakeMoneySTM.InsertMoney(self)    #instanta stare inserare
        self.current_state = self.wait_state  #starea curenta e asteptare
        self.money = 0  #suma introdusa initial zero

    def on_event(self, event, value=None):  #metoda de intrare eveniment
        self.current_state = self.current_state.on_event(event, value)  #schimbam stare dupa eveniment

    def add_money(self, amount: int):
        #wrapper pentru eveniment de inserare moneda
        self.on_event('insert_coin', amount)

    def client_arrived(self):
        #wrapper pentru eveniment client sosit
        self.on_event('client_arrived')

    def reset(self):
        #resetam automatul pentru o noua sesiune
        self.money = 0
        self.current_state = self.wait_state

class SelectProductSTM(Observable):  #automat pentru selectarea produsului
    class State(ABC):  #interfata de stare
        def __init__(self, machine):
            self.machine = machine
        @abstractmethod
        def choose(self, product_name: str):  #procesare selectie
            pass

    class SelectProduct(State):  #stare unica: alegere produs
        prices = {'Coca-Cola': 120, 'Pepsi': 100, 'Sprite': 90}  #lista preturi
        def choose(self, product_name: str):
            price = SelectProductSTM.SelectProduct.prices.get(product_name)
            if price is None:  #produs necunoscut
                print(f"Produs necunoscut: {product_name}")
                return self  #ramanem in stare
            self.machine.notify_all(product_name, price)  #notificam despre alegere
            return self  #ramanem in stare

    def __init__(self):
        super().__init__()
        self.select_product_state = SelectProductSTM.SelectProduct(self)  #instanta stare
        self.current_state = self.select_product_state  #starea curenta

    def choose(self, product_name: str):  #wrapper pentru selectie
        self.current_state = self.current_state.choose(product_name)

class VendingMachineSTM:  #clasa centrala care coordoneaza cele doua state machines si observatorii
    def __init__(self):
        self.take_money = TakeMoneySTM()  #automat bani
        self.select_product = SelectProductSTM()  #automat selectie

        self.display = DisplayObserver()  #afisaj suma
        self.choice = ChoiceObserver(self)  #notificare selectie produs

        self.take_money.attach(self.display)
        self.select_product.attach(self.choice)

    def start(self):  #initializare sesiune
        self.take_money.client_arrived()  #declansam evenimentul client sosit

    def insert_coin(self, amount: int):  #metoda apelata la inserare moneda
        print(f"Inserare {amount} bani")
        self.take_money.add_money(amount)  #trimit eveniment catre TakeMoneySTM

    def choose_product(self, product_name: str):  #metoda apelata la alegerea produsului
        print(f"Se apeleaza select_product: {product_name}")
        self.select_product.choose(product_name)  #trimit eveniment catre SelectProductSTM

    def proceed_to_checkout(self, product_name: str, price: int):  #validare tranzactie
        if self.take_money.money >= price:  #daca suma introdusa acopera pretul
            change = self.take_money.money - price  # calcul rest
            print(f"Produs vandut: {product_name}. Rest: {change} bani.")
            self.take_money.reset()  #resetam pentru o noua sesiune
        else:
            needed = price - self.take_money.money  #cat mai trebuie introdus
            print(f"Fonduri insuficiente. Mai inserati {needed} bani.")

if __name__ == '__main__':
    vm = VendingMachineSTM()  #cream instanta a masinii de sucuri
    vm.start()  #pornim sesiunea
    #simulam interactiune
    vm.insert_coin(50)  #client introduce 50 bani
    vm.insert_coin(50)  #client introduce inca 50 bani
    vm.choose_product('Pepsi')      #client alege Pepsi (100 bani)
    vm.choose_product('Sprite')     #client incearca Sprite, dar sesiunea s-a resetat
    vm.start()  #noua sesiune
    vm.insert_coin(200)  #client introduce 200 bani
    vm.choose_product('Coca-Cola')  #client alege Coca-Cola
    vm.choose_product('Sprite')     #selectie dupa finalizare sesiune, nu conteaza
