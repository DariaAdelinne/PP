import shlex
import subprocess

def run_pipeline(command_line):
    parts = [part.strip() for part in command_line.split('|')]
    commands = [shlex.split(part) for part in parts] #shelex.split pentru a converti fiecare iarte intr o lista de argumente

    prev_proc = None #pastreaza procesul anterior
    for i, cmd in enumerate(commands):
        if i == 0: #daca este prima comanda
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #lansam cu stdoutpentru capturarea iesirii si stderr pentru prinderea erorilor
        else: #pentru comenzi ulterioare
            proc = subprocess.Popen(
                cmd,
                stdin=prev_proc.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ) #se conecteaza la stdout, il seteaza si il ichide
            prev_proc.stdout.close()
        prev_proc = proc #actualizam referinta cu procesul curent

    out, err = prev_proc.communicate() #dupa ce s a executat ultimul proces se returneaza tuple
    return out, err

if __name__ == "__main__":
    cmd_line = input("Introduceti comanda cu pipe-uri: ")
    stdout, stderr = run_pipeline(cmd_line)

    if stdout: #daca exista iesirea standard sau erori le decodeaza si afiseaza
        print(stdout.decode().rstrip())
    if stderr:
        print("Eroare:", stderr.decode().rstrip())
