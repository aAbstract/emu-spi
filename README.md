# Emulated Serial Port Interface
This project provides an emulated serial port interface for testing purposes using socat.

## Usage
```
sudo socat -dd pty,raw,echo=0,link=/dev/ttyS90,mode=777 pty,raw,echo=0,link=/dev/ttyS91,mode=777
```
Sets up two pseudo-tty devices /dev/ttyUSB0 and /dev/ttyUSB1 using socat. These act as serial port terminals.

```
socat -dd TCP-LISTEN:6543,reuseaddr,fork FILE:/dev/ttyS91,raw,echo=0
```
Opens a TCP socket on port 6543 using socat that connects to /dev/ttyUSB0. This allows external applications to connect and communicate over the virtual bus.

```
python ./emu_spi.py
```
This will open the GUI window. Click "Connect" to connect to the VSPI server.  
The GUI allows sending commands and displays logging information.

You can then send these commands:
```js
cmd_map = {
    'vspic': pywebview.api.vspi_connect,
    'wjs': pywebview.api.soc_write_json,
    'wjsr': pywebview.api.soc_write_json_retain,
    'wdpw': pywebview.api.soc_write_device_packet_wght,
    'wdpr': pywebview.api.soc_write_device_packet_err,
    'exit': pywebview.api.exit,
};
```
