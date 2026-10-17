# first_monitor.py - watch the Engine think. For your first steps with Homylon.
# Run it on the computer where the Engine runs:  python3 first_monitor.py   (stop it with ctrl-C)
import json, socket, time

ENGINE = "127.0.0.1"   # the Engine runs on this computer (on another computer: the Engine's address)
MY_ADDRESS = "127.0.0.1"   # where this monitor runs (on another computer: its own address)
PORT = 55261           # where the Engine sends its lines to this monitor (engine_watch.py uses 55260)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.settimeout(1)
print("Waiting for the Engine. Stop with ctrl-C.")

last_registered = 0
while True:
    if time.time() - last_registered >= 1:         # say hello every second, so we see the Engine start
        hello = {"action": "registermonitor", "monitor": {
            "name": "firstmonitor", "address": MY_ADDRESS, "port": PORT,
            "protocol": "udp", "types": "all"}}
        sock.sendto(json.dumps(hello).encode(), (ENGINE, 55051))
        last_registered = time.time()
    try:
        data, _ = sock.recvfrom(65535)
        line = json.loads(data)
        print(f'{line.get("monitorMessageType", ""):8} {line.get("monitorMessageText", "")}')
    except (socket.timeout, ValueError):
        pass
