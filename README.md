# Homylon examples

Small, readable examples for Homylon: scenes for the language, and programs that talk to the engine.

**Homylon** is a home automation language and engine you can read: plain-text scenes that say how a
house should behave. Downloads, the manual and the Homylon engine: **[homylon.org](https://www.homylon.org)**.

## Scenes

Each folder is a package: open it in the Homylon engine. The names (lamps, sensors, phones) are those
of the Jensens, the family in the manual; use the names of your own house. Lamps and sensors from
agents such as the Hue agent announce themselves, so the scenes do not define them.

| Package | What it shows |
|---|---|
| [FrontDoor](scenes/FrontDoor.homylon/home.scene) | somebody at the door: who hears about it, and how, depends on who is home, the time of day and the holiday switch |
| [SunUpSunDown](scenes/SunUpSunDown.homylon/home.scene) | curtains and lamps that follow the sun all year, without a single clock time to change |
| [PowerBands](scenes/PowerBands.homylon/home.scene) | one lamp shows whether the house takes power from the grid or delivers it back |

## Python

Python 3, nothing to install.

| File | What it shows |
|---|---|
| [first_monitor.py](python/first_monitor.py) | watch the engine think: register as a monitor and print every line it sends (27 lines) |
| [virtual_lamp.py](python/virtual_lamp.py) | a complete agent: a lamp that lives in your terminal as a coloured block, and a motion sensor you trigger with the Enter key |

```sh
python3 python/first_monitor.py
python3 python/virtual_lamp.py
```

Both talk to an engine on the same computer; on another computer, change `ENGINE` and `MY_ADDRESS`
at the top of the file. With the virtual lamp running, try a scene:

```text
sub red by FF0000
when motion on virtualmotion then light virtuallamp on red brightness 80
```

## Swift

| Folder | What it shows |
|---|---|
| [swift/MiniMonitor](swift/MiniMonitor) | first_monitor.py in Swift, with [HomylonKit](https://github.com/Homylon/homylon-kit-swift) (Mac and Linux) |

```sh
cd swift/MiniMonitor
swift run MiniMonitor                 # the engine on this computer
swift run MiniMonitor 192.168.1.10    # the engine on another computer
```

## More

- How programs talk to the engine: [homylon-protocol](https://github.com/Homylon/homylon-protocol)
- A complete app: [homylon-monitor](https://github.com/Homylon/homylon-monitor)
- The language, step by step: the manual on [homylon.org](https://www.homylon.org)

## Licence

MIT, see LICENSE.
