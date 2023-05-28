import subprocess
import platform

def main():
    python_command = 'python3' if platform.system() == 'Darwin' else 'python'
    
    server_process = subprocess.Popen([python_command, 'Server.py'])
    gui_process = subprocess.Popen([python_command, 'GUI.py'])

    server_process.communicate()
    gui_process.communicate()

if __name__ == '__main__':
    main()
