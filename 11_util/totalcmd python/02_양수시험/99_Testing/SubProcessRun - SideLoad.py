import subprocess
from threading import Timer

def run_command_with_timeout(command, timeout_sec):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = Timer(timeout_sec, process.kill)

    try:
        timer.start()
        stdout, stderr = process.communicate()
    finally:
        timer.cancel()

    return stdout, stderr


# Example usage:
command = ['python.exe', 'timer.py', 'arg2']
timeout_seconds = 10

stdout, stderr = run_command_with_timeout(command, timeout_seconds)

# Use stdout and stderr as needed
print("Standard Output:", stdout.decode())
print("Standard Error:", stderr.decode())
