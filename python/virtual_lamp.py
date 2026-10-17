# virtual_lamp.py - a Homylon agent in one file: a lamp that lives in your terminal, and a motion
# sensor you trigger with the Enter key. No hardware needed.
#
#   python3 virtual_lamp.py        (stop it with ctrl-C)
#
# Then, in a scene:
#   sub red by FF0000
#   when motion on virtualmotion then light virtuallamp on red brightness 80
#   light virtuallamp off
import json, socket, struct, threading, time

ENGINE = "127.0.0.1"     # the Engine runs on this computer (on another computer: the Engine's address)
MY_ADDRESS = "127.0.0.1" # where this agent runs (on another computer: its own address)
MY_PORT = 55300          # where the Engine sends commands to this agent
AGENT = "virtual"        # the agent's name, as a scene can use it: define agent virtual ...

lamp = {"on": False, "brightness": 100, "color": "FFD8A0"}

def send_udp(message):                         # small messages: one UDP datagram each
    sock.sendto(json.dumps(message).encode(), (ENGINE, 55051))

def send_tcp(message):                         # big messages: the length in 4 bytes, then the JSON
    data = json.dumps(message).encode()
    with socket.create_connection((ENGINE, 55050)) as connection:
        connection.sendall(struct.pack(">I", len(data)) + data)

def announce():                                # tell the Engine who we are and what we have
    me = {"agent": AGENT, "ipaddress": MY_ADDRESS, "ports": [{"networkProtocol": "udp", "port": MY_PORT}]}
    lights = [{"name": "virtuallamp", "type": "colorLight", "state": lamp}]
    sensors = [{"name": "virtualmotion", "type": "motion", "state": {"presence": False}}]
    send_tcp({"action": "registeragent", "announcement": {"announce": dict(me, type="lights"), "list": lights}})
    send_tcp({"action": "registeragent", "announcement": {"announce": dict(me, type="sensors"), "list": sensors}})

def show():                                    # the lamp: a coloured block, as bright as the lamp
    if not lamp["on"]:
        print("lamp:  \033[48;2;40;40;40m        \033[0m  off")
        return
    r, g, b = (int(lamp["color"][i:i + 2], 16) * lamp["brightness"] // 100 for i in (0, 2, 4))
    print(f"lamp:  \033[48;2;{r};{g};{b}m        \033[0m  on, {lamp['brightness']}%, {lamp['color']}")

def motion():                                  # press Enter: motion, and a moment later no motion
    while True:
        input()
        send_udp({"action": "changedsensor", "name": "virtualmotion", "type": "motion", "status": True})
        print("motion!")
        time.sleep(1)
        send_udp({"action": "changedsensor", "name": "virtualmotion", "type": "motion", "status": False})

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", MY_PORT))
announce()
show()
threading.Thread(target=motion, daemon=True).start()
print("Press Enter for motion. Stop with ctrl-C.")

while True:
    message = json.loads(sock.recvfrom(65535)[0])
    action = message.get("action", "").lower().replace("_", "").replace("-", "")
    if action == "changelightstate":           # a command for the lamp
        if "onOff" in message: lamp["on"] = message["onOff"] == "on"
        if "brightness" in message: lamp["brightness"] = int(float(message["brightness"]))
        if "color" in message: lamp["color"] = message["color"].upper()
        show()
        report = {"action": "changedlight", "name": "virtuallamp", "state": "on" if lamp["on"] else "off",
                  "brightness": lamp["brightness"], "color": lamp["color"]}
        if "requestID" in message: report["requestID"] = message["requestID"]   # a remote asked: confirm it
        send_udp(report)
    elif action == "requestannouncement":      # the Engine (re)started and asks who is there
        announce()
    elif action == "agentrefused":             # this Engine's scene does not want us (accept / reject)
        print(f"The engine {message.get('home', '')} does not accept this agent.")
