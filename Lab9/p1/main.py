import subprocess
import sys
import os
import tempfile


class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def handle(self, content, filepath):
        if self._successor:
            return self._successor.handle(content, filepath)
        raise ValueError("Unknown file type; cannot execute.")


class PythonHandler(Handler):
    def handle(self, content, filepath):
        first = content.splitlines()[0] if content else ''
        if (first.startswith(
                "#!") and "python" in first) or 'def ' in content or 'import ' in content and filepath.endswith('.py'):
            return PythonCommand(filepath)
        return super().handle(content, filepath)


class BashHandler(Handler):
    def handle(self, content, filepath):
        first = content.splitlines()[0] if content else ''
        if (first.startswith("#!") and ("bash" in first or "sh" in first)) or content.strip().startswith("echo "):
            return BashCommand(filepath)
        return super().handle(content, filepath)


class JavaHandler(Handler):
    def handle(self, content, filepath):
        if 'public class ' in content and 'static void main' in content:
            for line in content.splitlines():
                line = line.strip()
                if line.startswith('public class '):
                    class_name = line.split()[2]
                    return JavaCommand(filepath, class_name)
        return super().handle(content, filepath)


class KotlinHandler(Handler):
    def handle(self, content, filepath):
        first = content.splitlines()[0] if content else ''
        if (first.startswith("#!") and "kotlin" in first) or 'fun main' in content:
            return KotlinCommand(filepath)
        return super().handle(content, filepath)


class Command:
    def execute(self):
        raise NotImplementedError


class PythonCommand(Command):
    def __init__(self, filepath): self.filepath = filepath

    def execute(self):
        res = subprocess.run(['python3', self.filepath], capture_output=True, text=True)
        return res.stdout + res.stderr


class BashCommand(Command):
    def __init__(self, filepath): self.filepath = filepath

    def execute(self):
        res = subprocess.run(['bash', self.filepath], capture_output=True, text=True)
        return res.stdout + res.stderr


class JavaCommand(Command):
    def __init__(self, filepath, class_name):
        self.filepath = filepath
        self.class_name = class_name
        self.workdir = tempfile.mkdtemp()

    def execute(self):
        java_file = os.path.join(self.workdir, self.class_name + '.java')
        open(java_file, 'w').write(open(self.filepath).read())
        subprocess.run(['javac', java_file], cwd=self.workdir)
        res = subprocess.run(['java', '-cp', self.workdir, self.class_name], capture_output=True, text=True)
        return res.stdout + res.stderr


class KotlinCommand(Command):
    def __init__(self, filepath): self.filepath = filepath

    def execute(self):
        res = subprocess.run(['kotlin', self.filepath], capture_output=True, text=True)
        return res.stdout + res.stderr


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <Fisiere>")
        sys.exit(1)
    path = sys.argv[1]
    # Construim lanțul de handler-e o singură dată
    handler_chain = PythonHandler(
        BashHandler(
            JavaHandler(
                KotlinHandler(None)
            )
        )
    )
    # Lista de căi: fișier sau toate fișierele din director
    targets = []
    if os.path.isdir(path):
        for name in sorted(os.listdir(path)):
            fp = os.path.join(path, name)
            if os.path.isfile(fp):
                targets.append(fp)
    else:
        targets.append(path)
    # Procesăm fiecare fișier
    for filepath in targets:
        print(f"--- Executing: {filepath} ---")
        try:
            content = open(filepath).read()
            cmd = handler_chain.handle(content, filepath)
            output = cmd.execute()
            print(output)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()