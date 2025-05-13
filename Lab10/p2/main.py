import threading
import queue

# Pipeline processing pentru un vector de intregi:
# 1) Inmultire cu o constanta alpha
# 2) Sortare
# 3) Afisare
# Fiecare etapa ruleaza intr-un thread separat si comunica prin queue-uri.

# Etapa 1: inmulteste fiecare element al vectorului cu alpha
def multiply_stage(V, out_q, alpha):
    # Preluam vectorul initial V
    result = [x * alpha for x in V]
    print(f"[Stage1] Vector inmultit cu {alpha}: {result}")
    # Trimitem rezultatul catre urmatoarea etapa
    out_q.put(result)
    # Semnal de sfarsit de date
    out_q.put(None)

# Etapa 2: sorteaza vectorul primit
def sort_stage(in_q, out_q):
    while True:
        data = in_q.get()          # asteptam date de la etapa anterioara
        if data is None:           # daca primim semnalul None, transmitem mai departe si iesim
            out_q.put(None)
            break
        sorted_data = sorted(data) # sortam lista
        print(f"[Stage2] Vector sortat: {sorted_data}")
        out_q.put(sorted_data)     # trimitem catre etapa urmatoare

# Etapa 3: afiseaza vectorul final
def display_stage(in_q):
    while True:
        data = in_q.get()
        if data is None:           # iesim la semnalul None
            break
        print(f"[Stage3] Vectorul final: {data}")

# Functia principala care initializeaza pipeline-ul
def main():
    # exemplu de vector si constanta
    V = [5, 2, 9, 1, 7]
    alpha = 10

    # cream doua queue-uri pentru comunicare intre etape
    q1 = queue.Queue()
    q2 = queue.Queue()

    # cream thread-urile pentru fiecare etapa
    t1 = threading.Thread(target=multiply_stage, args=(V, q1, alpha))
    t2 = threading.Thread(target=sort_stage, args=(q1, q2))
    t3 = threading.Thread(target=display_stage, args=(q2,))

    # pornim thread-urile
    t1.start()
    t2.start()
    t3.start()

    # asteptam finalizarea tuturor etapelor
    t1.join()
    t2.join()
    t3.join()

    print("[Main] Pipeline complet executat.")

if __name__ == '__main__':
    main()
