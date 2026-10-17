// MiniMonitor: register with the engine as a monitor, and print every line it sends.
// The same thing first_monitor.py does in Python, here with HomylonKit.

import Foundation
import HomylonKit

setvbuf(stdout, nil, _IOLBF, 0)   // print each line at once, also into a file or a pipe

let engine = CommandLine.arguments.dropFirst().first ?? "127.0.0.1"
let enginePort = 55051     // the engine's UDP port
let myPort: UInt16 = 55262 // where the engine sends its lines to this monitor

/// Prints what arrives: {"monitorMessageType": "Event", "monitorMessageText": "...", ...}
final class Printer: UDPServerDelegate {
    func udpDidReceiveData(_ data: Data?, from: String) {
        guard let data, let line = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else { return }
        let type = line["monitorMessageType"] as? String ?? ""
        let text = line["monitorMessageText"] as? String ?? ""
        print(type.padding(toLength: 8, withPad: " ", startingAt: 0), text)
    }
    func udpDidFailToStartWithError(_ error: Error) { print("Cannot listen on port \(myPort): \(error)"); exit(1) }
    func udpDidStartSuccessfully(onPort: Int) { print("Listening on UDP \(onPort). Stop with ctrl-C.") }
}

let printer = Printer()
let server = UDPServer()
server.delegate = printer
server.start(onPort: myPort, queue: .main)

// Register, and again every 3 seconds: the heartbeat. The engine stops sending to a monitor
// that misses three beats, so a monitor that stops simply disappears.
func register() {
    let me = localAddress(toward: engine) ?? "127.0.0.1"   // our address, as the engine can reach it
    Homylon.send(["action": "registermonitor",
                  "monitor": ["name": "minimonitor", "address": me, "port": Int(myPort),
                              "protocol": "udp", "types": "all", "heartbeat": 3]],
                 to: engine, port: enginePort)
}
register()
Timer.scheduledTimer(withTimeInterval: 3, repeats: true) { _ in register() }
RunLoop.main.run()
