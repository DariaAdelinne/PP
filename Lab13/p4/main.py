from functools import reduce
import math

is_prime = lambda n: n > 1 and all(n % d for d in range(2, int(math.sqrt(n)) + 1))

cond0 = lambda lst: any(map(lambda x: not is_prime(x), lst))
cond1 = lambda lst: any(map(lambda x: x % 2 == 0, lst))
cond2 = lambda lst: any(map(lambda x: x > 50, lst))

def run_automaton(lst):
    state = 0
    history = []
    current = lst

    while True:
        history.append((state, current.copy()))
        if state == 0 and cond0(current):
            state = 1
        elif state == 1 and cond1(current):
            state = 2
        elif state == 2 and cond2(current):
            state = 3
        else:
            break

    print("STOP: lista finala =", current)
    return history

input_list = [15, 22, 4, 51, 17, 60, 7, 80, 13]
trace = run_automaton(input_list)

for st, lst in trace:
    print(f"State {st} → {lst}")
