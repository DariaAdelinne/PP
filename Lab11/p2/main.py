import shlex
import subprocess

def run_pipeline(command_line):
    parts = [part.strip() for part in command_line.split('|')]
    commands = [shlex.split(part) for part in parts]

    prev_proc = None
    for i, cmd in enumerate(commands):
        if i == 0:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            proc = subprocess.Popen(
                cmd,
                stdin=prev_proc.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            prev_proc.stdout.close()
        prev_proc = proc

    out, err = prev_proc.communicate()
    return out, err

if __name__ == "__main__":
    cmd_line = input("Introduceti comanda cu pipe-uri: ")
    stdout, stderr = run_pipeline(cmd_line)

    if stdout:
        print(stdout.decode().rstrip())
    if stderr:
        print("Eroare:", stderr.decode().rstrip())
