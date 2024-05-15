# import subprocess
# import threading

# def start_fastapi():
#     subprocess.run(["poetry", "run", "uvicorn", "src.oai_agent.oai_agent:app", "--reload"])

# def start_vnc_container():
#     subprocess.run(["docker", "run", "-p", "6080:6080", "my-vnc-server"])

# def main():
#     fastapi_thread = threading.Thread(target=start_fastapi)
#     vnc_thread = threading.Thread(target=start_vnc_container)

#     fastapi_thread.start()
#     vnc_thread.start()

#     fastapi_thread.join()
#     vnc_thread.join()

# if __name__ == "__main__":
#     main()

import subprocess
import threading
import time

def start_fastapi():
    subprocess.run(["poetry", "run", "uvicorn", "src.oai_agent.oai_agent:app", "--reload"])

def start_vnc_container():
    port = 6080
    while True:
        result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
        if result.stdout:
            port += 1
        else:
            break
    
    subprocess.run(["docker", "run", "-p", f"{port}:6080", "my-vnc-server"])

def main():
    fastapi_thread = threading.Thread(target=start_fastapi)
    vnc_thread = threading.Thread(target=start_vnc_container)

    fastapi_thread.start()
    vnc_thread.start()

    fastapi_thread.join()
    vnc_thread.join()

if __name__ == "__main__":
    main()
