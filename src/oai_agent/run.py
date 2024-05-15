import subprocess
import threading
import time

def start_fastapi():
    subprocess.run(["poetry", "run", "uvicorn", "src.oai_agent.oai_agent:app", "--reload"])

def start_vnc_server():
    import websockify
    import novnc
    websockify_server = websockify.WebSocketServer("localhost", 8080)
    novnc_server = novnc.NoVNCServer("localhost", 5900)
    websockify_server.start()
    novnc_server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        websockify_server.stop()
        novnc_server.stop()

def main():
    fastapi_thread = threading.Thread(target=start_fastapi)
    vnc_thread = threading.Thread(target=start_vnc_server)

    fastapi_thread.start()
    vnc_thread.start()

    fastapi_thread.join()
    vnc_thread.join()

if __name__ == "__main__":
    main()
