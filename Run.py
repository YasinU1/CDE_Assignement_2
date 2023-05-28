import subprocess
import platform

def main():
    # We pick the right way to run Python depending on 
    # your computer - Heterogeneous systems architectures (i.e., different O/S)
    python_command = 'python3' if platform.system() == 'Darwin' else 'python'

    # Try to start the server
    try:
        server_process = subprocess.Popen([python_command, 'Server.py'])
    except Exception as e:
        # If something went wrong, print out the problem
        print(f"Oops! We had trouble starting the server: {e}")
        return  # End the program

    # Try to start the client
    try:
        gui_process = subprocess.Popen([python_command, 'Client.py'])
    except Exception as e:
        # If something went wrong, print out the problem
        print(f"Oops! We had trouble starting the client: {e}")
        return  # End the program

    # Wait for both the server and client to finish running
    server_process.communicate()
    gui_process.communicate()

if __name__ == '__main__':
    main()
