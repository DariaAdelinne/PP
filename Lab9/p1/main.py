import subprocess  
import sys      
import os        
import tempfile   

class Handler:
    def __init__(self, successor=None):
        #successor este urmatorul handler in lant
        self._successor = successor

    def handle(self, content, filepath):
        #daca nu putem procesa, delegam urmatorului handler
        if self._successor:
            return self._successor.handle(content, filepath)
        #daca am ajuns la final si nimeni nu stie sa proceseze, ridicam eroare
        raise ValueError("Unknown file type; cannot execute.")

class PythonHandler(Handler):
    def handle(self, content, filepath):
        #preluam prima linie pentru shebang daca exista
        first = content.splitlines()[0] if content else ''
        #detectam fie shebang cu python, fie prezenta unui def/import sau extensie .py
        if ((first.startswith("#!") and "python" in first)
                or 'def ' in content
                or ('import ' in content and filepath.endswith('.py'))):
            return PythonCommand(filepath)  #returnam un obiect PythonCommand
        #daca nu s-a potrivit, apelam handler-ul urmator
        return super().handle(content, filepath)

class BashHandler(Handler):
    def handle(self, content, filepath):
        first = content.splitlines()[0] if content else ''
        #detectam shebang bash/sh sau un comando echo in prima coloana
        if ((first.startswith("#!") and ("bash" in first or "sh" in first))
                or content.strip().startswith("echo ")):
            return BashCommand(filepath)
        return super().handle(content, filepath)

class JavaHandler(Handler):
    def handle(self, content, filepath):
        #verificam prezenta "public class" si "static void main"
        if 'public class ' in content and 'static void main' in content:
            #parcurgem fiecare linie pentru a extrage numele clasei
            for line in content.splitlines():
                line = line.strip()
                if line.startswith('public class '):
                    #tokenizam si luam al treilea cuvant ca nume de clasa
                    class_name = line.split()[2]
                    return JavaCommand(filepath, class_name)
        return super().handle(content, filepath)

class KotlinHandler(Handler):
    def handle(self, content, filepath):
        first = content.splitlines()[0] if content else ''
        #detectam shebang kotlin sau prezenta functiei main in Kotlin
        if ((first.startswith("#!") and "kotlin" in first)
                or 'fun main' in content):
            return KotlinCommand(filepath)
        return super().handle(content, filepath)

class Command:
    def execute(self):
        #fiecare comanda concreta trebuie sa implementeze execute()
        raise NotImplementedError

class PythonCommand(Command):
    def __init__(self, filepath):
        self.filepath = filepath  #retinem calea fisierului

    def execute(self):
        #folosim un process extern care ruleaza Python 3
        res = subprocess.run(
            ['python3', self.filepath],  #comanda si argument
            capture_output=True, text=True  #capturam stdout+stderr ca text
        )
        return res.stdout + res.stderr  #returnam output-ul combinat

class BashCommand(Command):
    def __init__(self, filepath):
        self.filepath = filepath

    def execute(self):
        #rulam fisierul cu bash
        res = subprocess.run(
            ['bash', self.filepath],
            capture_output=True, text=True
        )
        return res.stdout + res.stderr

class JavaCommand(Command):
    def __init__(self, filepath, class_name):
        self.filepath = filepath
        self.class_name = class_name
        #cream un director temporar pentru fisierele .java si .class
        self.workdir = tempfile.mkdtemp()

    def execute(self):
        #copiem continutul .java intr-un fisier in workdir
        java_file = os.path.join(self.workdir, self.class_name + '.java')
        open(java_file, 'w').write(open(self.filepath).read())
        #compilam cu javac in directorul temporar
        subprocess.run(['javac', java_file], cwd=self.workdir)
        #rulam clasa compilata cu java
        res = subprocess.run(
            ['java', '-cp', self.workdir, self.class_name],
            capture_output=True, text=True
        )
        return res.stdout + res.stderr

class KotlinCommand(Command):
    def __init__(self, filepath):
        self.filepath = filepath

    def execute(self):
        #rulam cu interpretul Kotlin (trebuie instalat in sistem)
        res = subprocess.run(
            ['kotlin', self.filepath],
            capture_output=True, text=True
        )
        return res.stdout + res.stderr

def main():
    #verificam numarul de argumente: trebuie exact 1 (cale fisier sau director)
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <Fisiere>")
        sys.exit(1)
    path = sys.argv[1]
    #construim lantul de handler-e o singura data
    handler_chain = PythonHandler(
        BashHandler(
            JavaHandler(
                KotlinHandler(None)
            )
        )
    )
    #colectam toate tintele (fisier sau fisiere din director)
    targets = []
    if os.path.isdir(path):
        for name in sorted(os.listdir(path)):
            fp = os.path.join(path, name)
            if os.path.isfile(fp):
                targets.append(fp)
    else:
        targets.append(path)
    #procesam fiecare fisier in ordine
    for filepath in targets:
        print(f"--- Executing: {filepath} ---")  #afisam fisierul curent
        try:
            content = open(filepath).read()  #citim tot continutul
            cmd = handler_chain.handle(content, filepath)  #obtinem comanda potrivita
            output = cmd.execute()  #executam comanda
            print(output)  #afisam output-ul
        except Exception as e:
            print(f"Error: {e}")  #in caz de eroare, afisam mesajul
if __name__ == '__main__':
    main()
