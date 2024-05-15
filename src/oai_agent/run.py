
import subprocess
import threading

def start_fastapi():
    subprocess.run(["poetry", "run", "uvicorn", "src.oai_agent.oai_agent:app", "--reload"])

def start_vnc_client():
    subprocess.run(["docker", "run", "-p", "6080:6080", "my-vnc-server"])

def main():
    fastapi_thread = threading.Thread(target=start_fastapi)
    vnc_thread = threading.Thread(target=start_vnc_client)

    fastapi_thread.start()
    vnc_thread.start()

    fastapi_thread.join()
    vnc_thread.join()

if __name__ == "__main__":
    main()
