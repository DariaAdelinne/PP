from abc import ABC, abstractmethod

# Observer Pattern
class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass

class Observable:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify_all(self, *args, **kwargs):
        for obs in self._observers:
            obs.update(*args, **kwargs)

# Observers concreti
class DisplayObserver(Observer):
    def update(self, money: int):
        print(f"[Display] Suma introdusa: {money} bani")

class ChoiceObserver(Observer):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def update(self, product_name: str, price: int):
        print(f"[Choice] A fost selectat produsul: {product_name} (pret {price} bani)")
        # Notificăm automatul central să verifice tranzacția
        self.vending_machine.proceed_to_checkout(product_name, price)

# TakeMoney State Machine
class TakeMoneySTM(Observable):
    class State(ABC):
        def __init__(self, machine):
            self.machine = machine
        @abstractmethod
        def on_event(self, event, value=None):
            pass

    class WaitingForClient(State):
        def on_event(self, event, value=None):
            if event == 'client_arrived':
                print("Client ajuns. Astept inserare bani.")
                return self.machine.insert_state
            return self

    class InsertMoney(State):
        def on_event(self, event, value=None):
            if event == 'insert_coin':
                self.machine.money += value
                # notify display
                self.machine.notify_all(self.machine.money)
                return self
            return self

    def __init__(self):
        super().__init__()
        self.wait_state = TakeMoneySTM.WaitingForClient(self)
        self.insert_state = TakeMoneySTM.InsertMoney(self)
        self.current_state = self.wait_state
        self.money = 0

    def on_event(self, event, value=None):
        self.current_state = self.current_state.on_event(event, value)

    def add_money(self, amount: int):
        # eveniment generic pentru inserare monedă
        self.on_event('insert_coin', amount)

    def client_arrived(self):
        self.on_event('client_arrived')

    def reset(self):
        self.money = 0
        self.current_state = self.wait_state

# SelectProduct State Machine
class SelectProductSTM(Observable):
    class State(ABC):
        def __init__(self, machine):
            self.machine = machine
        @abstractmethod
        def choose(self, product_name: str):
            pass

    class SelectProduct(State):
        prices = {'Coca-Cola': 120, 'Pepsi': 100, 'Sprite': 90}
        def choose(self, product_name: str):
            price = SelectProductSTM.SelectProduct.prices.get(product_name)
            if price is None:
                print(f"Produs necunoscut: {product_name}")
                return self
            # notifică alegerea
            self.machine.notify_all(product_name, price)
            return self

    def __init__(self):
        super().__init__()
        self.select_product_state = SelectProductSTM.SelectProduct(self)
        self.current_state = self.select_product_state

    def choose(self, product_name: str):
        self.current_state = self.current_state.choose(product_name)

# Vending Machine Central
class VendingMachineSTM:
    def __init__(self):
        self.take_money = TakeMoneySTM()
        self.select_product = SelectProductSTM()
        # atașăm observatori
        self.display = DisplayObserver()
        self.choice = ChoiceObserver(self)
        self.take_money.attach(self.display)
        self.select_product.attach(self.choice)

    def start(self):
        # inițierea secvenței
        self.take_money.client_arrived()

    def insert_coin(self, amount: int):
        print(f"Inserare {amount} bani")
        self.take_money.add_money(amount)

    def choose_product(self, product_name: str):
        print(f"Se apeleaza select_product: {product_name}")
        self.select_product.choose(product_name)

    def proceed_to_checkout(self, product_name: str, price: int):
        # verifică fonduri
        if self.take_money.money >= price:
            change = self.take_money.money - price
            print(f"Produs vandut: {product_name}. Rest: {change} bani.")
            # resetăm pentru o nouă sesiune
            self.take_money.reset()
        else:
            needed = price - self.take_money.money
            print(f"Fonduri insuficiente. Mai inserati {needed} bani.")

# Exemplu de utilizare
if __name__ == '__main__':
    vm = VendingMachineSTM()
    vm.start()
    # Simulare interacțiune
    vm.insert_coin(50)
    vm.insert_coin(50)
    vm.choose_product('Pepsi')      # 100 bani
    # Alegem alt produs
    vm.choose_product('Sprite')     # 90 bani, dar contorul a fost resetat
    # Pornim o nouă sesiune
    vm.start()
    vm.insert_coin(200)
    vm.choose_product('Coca-Cola')  # 120 bani
    vm.choose_product('Sprite')     # nu contează, sesiune finalizată
