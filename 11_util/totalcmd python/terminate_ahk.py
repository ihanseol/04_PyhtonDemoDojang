import psutil
import os

# Define the process name pattern to match
process_name_pattern = "autohotkey"

# Iterate over all running processes
for proc in psutil.process_iter(['pid', 'name']):
    try:
        # Check if the process name starts with the defined pattern
        if proc.info['name'].lower().startswith(process_name_pattern.lower()) and proc.info['name'].lower().endswith('.exe'):
            # Terminate the process
            os.kill(proc.info['pid'], 9)
            print(f"Terminated: {proc.info['name']} (PID: {proc.info['pid']})")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

print("All processes matching the pattern have been terminated.")
