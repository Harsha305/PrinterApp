import subprocess
import os

def get_connected_printers():
    try:
        process = subprocess.Popen(['lpstat', '-p'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error and error.decode().strip():
            return []

        printer_names = []
        for line in output.decode().split('\n'):
            if line.startswith('printer'):
                printer_name = line.split(' ')[1]
                printer_names.append(printer_name)
        return printer_names

    except Exception:
        return []

def print_file(printer_name, file_path):
    if not os.path.isfile(file_path):
        return False, f"Error: File '{file_path}' does not exist."

    try:
        process = subprocess.Popen(['lp', '-d', printer_name, file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            return True, "Print job submitted successfully."
        else:
            return False, error.decode().strip()
    except Exception as e:
        return False, str(e)
